# -*- coding: utf-8 -*-
import os
import sys
import asyncio
import pytest

sys.path.insert(0, os.path.dirname(os.getcwd()))
from create_currency_df_async import create_currency_df, fetch


"""
TESTS: pytest .\get_currency_test.py
"""

@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


def test_get_the_df_responses(event_loop) :

    assert event_loop.run_until_complete(create_currency_df(20150808)) == 'x'
    assert event_loop.run_until_complete(create_currency_df(20150808000000)) == 'x'
    assert event_loop.run_until_complete(create_currency_df('')) == 'x'
    assert event_loop.run_until_complete(create_currency_df('2020/05')) == 'x'

    df_response = event_loop.run_until_complete(create_currency_df(20200812))
    assert df_response['Pais'][-1].strip() == 'CHILE'
    assert df_response['Pais'][23].strip() == 'RUANDA'




