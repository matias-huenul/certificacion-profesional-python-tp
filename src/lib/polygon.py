import requests
import os

POLYGON_API_URL = "https://api.polygon.io/v3/reference/tickers"

class TooManyRequestsError(Exception):
    pass

class NotFoundError(Exception):
    pass

def get_ticker(ticker, date):
    """
    Devuelve información acerca del ticker para la fecha
    especificada.
    En caso de error en la respuesta, lanza
    una excepción (TooManyRequestsError o NotFoundError).
    """
    api_key = os.environ.get("POLYGON_API_KEY")
    if not api_key:
        raise Exception("No existe la variable de entorno POLYGON_API_KEY")
    response = requests.get(url=f"{POLYGON_API_URL}/{ticker}", params={
            "apiKey": api_key,
            "date": date
    })
    if response.status_code == 429:
        raise TooManyRequestsError
    if response.status_code == 404:
        raise NotFoundError
    data = response.json()
    result =  data["results"]
    return {
        "symbol": result["ticker"],
        "name": result["name"],
        "value": result["market_cap"] / result["weighted_shares_outstanding"],
        "date": date,
    }
