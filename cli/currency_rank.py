#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,os
import argparse
from time import time
import asyncio

sys.path.insert(0, os.path.dirname(os.getcwd()))
from create_currency_df_async import create_currency_df



if __name__ == "__main__":
    start = time()

    # CLI
    # parser = argparse.ArgumentParser(description='Returns worst currency relative to USD from Central Bank of Brazil quotation date')
    # parser.add_argument('date', metavar='[ISO Timestamp eg: 20200810]', type=int,
    #                     help='The market date to search. eg: 20200810 or 20150812')
    # args = parser.parse_args()

    loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(create_currency_df(args.date))
    result = loop.run_until_complete(create_currency_df(20150808))

    # treats 'x' or bad formatted files
    try:
        # RANKS
        result = result[:1]

        # formatting result to CLI
        currency_symbol = f" {result['Pais'].index[0]}"
        country = result['Pais'][0].strip()
        usd_to_currency = str(result['USD to Currency'][0].round(3))
        cli_result = [currency_symbol, country, usd_to_currency]
    except:
       cli_result = 'x'

    print("\n=====================================")
    print(', '.join(cli_result))
    print("=====================================\n")

    print(f"Process took: {time() - start} seconds")

    # bug 20150808