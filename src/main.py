#! /usr/bin/env python3

"""
Certificación Profesional en Python (ITBA) | Trabajo Práctico Final
Alumno: Matías Huenul
"""

import os
import requests
import lib.utils as utils
import lib.exceptions as exc
import lib.polygon as polygon
from datetime import datetime

POLYGON_API_TOKEN = None

def setup():
    """
    Configura las variables necesarias para la ejecución
    del programa. Lanza una excepción en caso de detectar
    algún error de configuración.
    """
    try:
        POLYGON_API_TOKEN = os.environ["POLYGON_API_TOKEN"]
    except KeyError:
        raise SetupError

def get_tickers(ticker, start_date, end_date):
    """
    Realiza una llamada a la API de Ticker y devuelve
    el resultado.
    """
    results = []
    start = datetime.strptime(start_date, "%Y/%m/%d")
    end = datetime.strptime(end_date, "%Y/%m/%d")
    for date in utils.get_date_range(start, end):
        data = polygon.get_ticker(
            ticker, POLYGON_API_TOKEN, date.strftime("%Y-%m-%d"))
        if data["status"] != "OK":
            raise exc.APIError
        results.append(data["results"])
    return results

def save_data_to_db(data):
    """
    Persiste información de tickers en la base
    de datos.
    """
    pass

def get_all_tickers():
    """
    Obtiene todos los tickers guardados
    en la base de datos.
    """
    pass

def make_ticker_plot(ticker):
    """
    Genera una visualización para un ticker.
    """
    pass

def handle_user_input():
    """
    Maneja el input del usuario mediante
    línea de comandos.
    """
    op = input(
        "Indique la operación a realizar:\n"
        "  1. Actualización de datos\n"
        "  2. Visualización de datos\n"
    )

    if op == "1":
        ticker = input("Ingrese ticker a pedir:\n")
        start_date = input("Ingrese fecha de inicio:\n")
        end_date = input("Ingrese fecha de fin:\n")
        print("Pidiendo datos...")
        data = make_api_request(ticker, start_date, end_date)
        save_data_to_db(data)
        print("Datos guardados correctamente")
    elif op == "2":
        op = input(
            "Indique la visualización a realizar:\n"
            "  1. Resumen\n"
            "  2. Gráfico de ticker\n"
        )
        if op == "1":
            tickers = get_all_tickers()
            print("Los tickers guardados en la base de datos son:")
            for ticker in tickers:
                print(ticker)
        elif op == "2":
            ticker = input("Ingrese el ticker a graficar:\n")
            plot = make_ticker_plot(ticker)
            # TODO: show plot
        else:
            raise exc.OperationError
    else:
        raise exc.OperationError

def main():
    """
    Función principal del programa.
    """
    try:
        setup()
        handle_user_input()
    except KeyboardInterrupt:
        print("\nCancelado")
    except exc.OperationError:
        print("Operación inválida")
    except Exception:
        print("Error inesperado")

if __name__ == "__main__":
    main()
