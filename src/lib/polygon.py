import requests
import os

POLYGON_API_URL = "https://api.polygon.io/v3/reference/tickers/AAPL"

def get_ticker(ticker, date):
    api_key = os.environ.get("POLYGON_API_KEY")
    if not api_key:
        raise Exception("No existe la variable de entorno POLYGON_API_KEY")
    response = requests.get(url=POLYGON_API_URL, params={
            "apiKey": api_key,
            "date": date
        })
    response.raise_for_status()
    data = response.json()
    status = data["status"]
    if status != "OK":
        raise Exception(f"Error de API (status={status})")
    result =  data["results"]
    return {
        "symbol": result["ticker"],
        "name": result["name"],
        "value": result["market_cap"] / result["weighted_shares_outstanding"],
        "date": date,
    }
