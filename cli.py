#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from time import time
from io import StringIO

import pandas as pd
import requests



def get_currecy_rank(date=None):
    """
    This Routine downloads from Brazil central bank site two csv files
    with currency information, preprocess then and generate a dataframe
    containing a rank of the worst currency relative to USD quotation

    :param date: iso format timestamp of a market date. eg: 20200811
    :return: Dataframe or Series with the currency information
    """

    try:
        ########################################################
        # FIRST DATAFRAME - ALL CURRENCIES VALUES AT MARKET CLOSE
        ########################################################

        currencies_prices_url = f"https://www4.bcb.gov.br/Download/fechamento/{date}.csv"

        data_from_url = StringIO(requests.get(currencies_prices_url).text)
        cols = ['Timestamp', 'Cod Moeda', 'Tipo', 'Moeda',
                'Taxa Compra', 'Taxa Venda', 'Paridade Compra',
                'Paridade Venda']
        df = pd.read_csv(data_from_url, sep=";", names=cols)

        # PREPROCESSING CURRENCY VALUES
        aux = df.set_index('Moeda')
        usd = aux.loc['USD']
        usd_value = float(usd['Taxa Compra'].replace(',', '.'))

        # Casting strings to float
        df["Taxa Compra"] = df["Taxa Compra"].str.replace(',', '.')
        df["Paridade Compra"] = df["Paridade Compra"].str.replace(',', '.')

        # new column with USD to Currency formula
        new_df = df.copy(deep=True)
        new_df['USD to Currency'] = usd_value / (new_df['Taxa Compra'].astype(float))

        # sorting by the formula result
        sorted_df = new_df.sort_values(by='USD to Currency', ascending=False)

        ########################################################
        # SECCOND DATAFRAME - CURRENCIES INFO VALUES AT MARKET CLOSE
        ########################################################

        info_currencies_url = f"https://www4.bcb.gov.br/Download/fechamento/M{date}.csv"
        cols = ['Codigo', 'Nome', 'Simbolo', 'Cod. Pais', 'Pais', 'Tipo', 'Data Exlusao Ptax']

        info_data_from_url = StringIO(requests.get(info_currencies_url).text)
        df_info = pd.read_csv(info_data_from_url, sep=";", names=cols, encoding="latin")
        # removes first row
        df_info = df_info.iloc[1 :]

        # FIXING THE EMPTY SPACES FROM 'Simbolo' column, as it will be our index matching criteria
        df_info['Simbolo'] = df_info['Simbolo'].astype(str)
        df_info["Simbolo"] = df_info["Simbolo"].str.replace(' ', '')

        ########################################################
        ### JOINING AND PREPROCESSING THE FINAL DATAFRAME
        ########################################################
        idx_sorted = sorted_df.set_index('Moeda')
        idx_info = df_info.set_index('Simbolo')
        merge_df = idx_sorted.join(idx_info, lsuffix='_left', on='Moeda')
        final_df = merge_df.copy(deep=True)

        # Removing non-countries tickets, unnecessary collumns and duplicates currencies
        final_cols = ['Nome', 'Cod Moeda', 'Pais', 'Taxa Compra', 'USD to Currency']
        final_df_aux = final_df[final_cols]
        filtered_df = final_df_aux[final_df_aux['Pais'].notnull()]
        unique_filtered_df = filtered_df.drop_duplicates(subset=['Cod Moeda'])

        # RANK
        worst_currency = unique_filtered_df[:1]
        result = worst_currency

        # formatting result to CLI
        currency_symbol = f" {result['Pais'].index[0]}"
        country = result['Pais'][0].strip()
        usd_to_currency = str(result['USD to Currency'][0].round(3))
        cli_result = [ currency_symbol, country, usd_to_currency ]

        return cli_result

    except Exception as e:
        return "x"




if __name__ == "__main__":
    start = time()

    parser = argparse.ArgumentParser(description='Returns worst currency relative to USD from Central Bank of Brazil quotation date')
    parser.add_argument('date', metavar='[ISO Timestamp eg: 20200810]', type=int,
                        help='The market date to search. eg: 20200810 or 20150812')
    args = parser.parse_args()

    result = get_currecy_rank(args.date)
    print("\n=====================================")
    print(', '.join(result))
    print("=====================================\n")

    # print(f"Process took: {time() - start} seconds")
    # TODO
    """
    Refactor to smaller function, tests, api, treat exception
    """