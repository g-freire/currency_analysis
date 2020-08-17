#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from time import time
from io import StringIO

import asyncio
import aiohttp
import pandas as pd


async def fetch(session, url):
    async with session.get(url) as response:
        return await (response.text())


async def download_preprocess_currency_quotation_df(date: int) -> pd.DataFrame:
    ########################################################
    # FIRST DATAFRAME - ALL CURRENCIES VALUES AT MARKET CLOSE
    ########################################################

    currencies_prices_url = f"https://www4.bcb.gov.br/Download/fechamento/{date}.csv"
    try:
        async with aiohttp.ClientSession() as session:
            data_from_url = await fetch(session,currencies_prices_url)
    except:raise
    else:
        cols = ['Timestamp', 'Cod Moeda', 'Tipo', 'Moeda',
                'Taxa Compra', 'Taxa Venda', 'Paridade Compra',
                'Paridade Venda']
        df = pd.read_csv(StringIO(data_from_url), sep=";", names=cols)

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

        return sorted_df


async def download_preprocess_currencies_info_df(date: int) -> pd.DataFrame:
    ########################################################
    # SECCOND DATAFRAME - CURRENCIES INFO VALUES AT MARKET CLOSE
    ########################################################

    info_currencies_url = f"https://www4.bcb.gov.br/Download/fechamento/M{date}.csv"
    try:
        async with aiohttp.ClientSession() as session:
            info_data_from_url = await fetch(session, info_currencies_url)
    except:raise

    else:
        cols = ['Codigo', 'Nome', 'Simbolo', 'Cod. Pais', 'Pais', 'Tipo', 'Data Exlusao Ptax']
        df_info = pd.read_csv(StringIO(info_data_from_url), sep=";", names=cols, encoding="latin")
        # removes first row
        df_info = df_info.iloc[1:]

        # FIXING THE EMPTY SPACES FROM 'Simbolo' column, as it will be our index matching criteria
        df_info['Simbolo'] = df_info['Simbolo'].astype(str)
        df_info["Simbolo"] = df_info["Simbolo"].str.replace(' ', '')

        return df_info


async def create_currency_df(date: int) -> pd.DataFrame:
    """
    This Routine downloads from Brazil central bank site two csv files
    with currency information, preprocess then and generate a dataframe
    containing a rank of the worst currency relative to USD quotation

    :param date: iso format timestamp of a market date. eg: 20200811
    :return: Dataframe or Series with the currency information
    """

    try:

        # schedules and executes concurrent async download tasks
        sorted_df_task = asyncio.create_task(
            download_preprocess_currency_quotation_df(date))

        df_info_task = asyncio.create_task(
            download_preprocess_currencies_info_df(date))

        sorted_df = await sorted_df_task
        df_info = await df_info_task

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

        return unique_filtered_df

    except Exception as e:
        return 'x'
        # return str(e)


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     result = loop.run_until_complete(create_currency_df(20200810))
