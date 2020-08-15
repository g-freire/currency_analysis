import sys
import os

from fastapi import FastAPI,HTTPException
import uvicorn

sys.path.insert(0, os.path.dirname(os.getcwd()))
from create_currency_df_async import create_currency_df
from models import CurrencyInfo


app = FastAPI(title="Currency Rank",
              description="API to return worst currency relative to USD from Central Bank of Brazil quotation date",
              version="1.0.0",)
    

@app.get("/get_worst_currency/{date}", response_model=CurrencyInfo, response_model_exclude_unset=True)
async def get_currency(date: int):

    result =  await create_currency_df(date)
    try:
        result = result[:1]
        currency_symbol = f" {result['Pais'].index[0]}"
        country = result['Pais'][0].strip()
        usd_to_currency = str(result['USD to Currency'][0].round(3))
        result = {
            "currency_symbol":currency_symbol,
            "country":country,
            "usd_to_currency":usd_to_currency,
        }
        return CurrencyInfo(**result)
    
    except Exception as e:
       raise HTTPException(status_code=401, detail=str(e))


# local, comment to deploy
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)