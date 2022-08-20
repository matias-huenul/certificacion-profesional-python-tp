import requests

POLYGON_API_URL = "https://api.polygon.io/v3/reference/tickers/AAPL"

def get_ticker(ticker, api_key, date):
    response = requests.get(url=POLYGON_API_URL, params={
            "apiKey": api_key,
            "date": date
        })
    response.raise_for_status()
    return response.json()
