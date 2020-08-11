#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from lxml import html
from time import time,sleep

"""
REF: https://github.com/echiesse/desafios_programacao/blob/master/004-Cotacao_moedas.md

https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/swagger-ui3#/
https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='08-10-2020'&$top=100&$format=json
https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?%40moeda='JPY'&%40dataCotacao='08-10-2020'&%24format=json" -H "accept: application/json;odata.metadata=minimal"

https://www3.bcb.gov.br/bc_moeda/rest/cotacao/fechamento/ultima/1/005/2020-08-05

https://www.bcb.gov.br/estabilidadefinanceira/cotacoestodas

ENDPOINT DOWNLOAD
https://www4.bcb.gov.br/Download/fechamento/20200810.csv

NOME PAISES
https://www.bcb.gov.br/estabilidadefinanceira/todasmoedas
https://www4.bcb.gov.br/Download/fechamento/M20200810.csv

"""

def get_currecy():
    return "ok"



if __name__ == "__main__":
    start = time()
    get_currecy()
    print(f"Process took: {time() - start} seconds")