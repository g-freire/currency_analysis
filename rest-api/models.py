from pydantic import BaseModel

class CurrencyInfo(BaseModel):
    currency_symbol: str
    country: str
    usd_to_currency: str