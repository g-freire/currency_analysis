#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from lxml import html
from time import time,sleep
import sys
from io import StringIO
import numpy as np
import pandas as pd
import requests
import datetime


def get_currecy_rank(date=None):
    """
    Routine to download from brazil central bank site two csv files
    with currency information, preprocess then and generate a dataframe
    containing a rank of the worst currency relative to USD current value

    :param date: iso format timestamp of a market date. eg: 20200811
    :return: string with currency
    """

    try:

        # FIRST DATAFRAME - ALL CURRENCIES VALUES AT MARKET CLOSE

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
        a = sorted_df.head(5)
        a   


        currencies_info_url = f"https://www4.bcb.gov.br/Download/fechamento/M{date}.csv"

        return date

    except Exception as e:
        print(str(e))




if __name__ == "__main__":
    start = time()
    get_currecy_rank(20200811)
    print(f"Process took: {time() - start} seconds")