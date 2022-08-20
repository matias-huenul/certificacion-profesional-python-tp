#! /usr/bin/env python3

"""
Certificación Profesional en Python (ITBA) | Trabajo Práctico Final
Alumno: Matías Huenul
"""

import os
import traceback
import requests
import sqlite3
import lib.utils as utils
import lib.database as db
import lib.exceptions as exc
import lib.polygon as polygon
from time import sleep
from datetime import datetime

def get_tickers(ticker, start_date, end_date):
    """
    Realiza una llamada a la API de Ticker y guarda
    los resultados en la base de datos.
    """
    print("Pidiendo datos...")
    tickers = []
    start = datetime.strptime(start_date, "%Y/%m/%d")
    end = datetime.strptime(end_date, "%Y/%m/%d")
    for date in utils.get_date_range(start, end):
        ticker = polygon.get_ticker(ticker, date.strftime("%Y-%m-%d"))
        tickers.append(ticker)
    for ticker in tickers:
        db.insert_ticker(ticker)
    print("Datos guardados correctamente")

def show_tickers():
    """
    Imprime un resumen de los tickers guardados en la base de datos.
    """
    print("Los tickers guardados en la base de datos son:")
    for ticker, min_date, max_date in db.fetch_stats_tickers():
        print(f"{ticker} - {min_date} <-> {max_date}")

def plot_ticker(ticker):
    """
    Grafica los datos guardados para un ticker específico.
    """
    # TODO: show plot
    pass

def prompt(message, options=[]):
    """
    Recibe input del usuario, el cual puede
    ser un texto o un valor dentro de posibles opciones.
    """
    message += ":\n"
    for i, option in enumerate(options):
        message += f"  {i + 1}. {option}\n"
    response = input(message)
    if not options:
        return response
    response = int(response)
    if response < 0 or response > len(options):
        raise exc.OperationError
    return response

def handle_user_input():
    """
    Maneja el input del usuario mediante
    línea de comandos.
    """
    op = prompt("Indique la operación a realizar", options=[
        "Actualización de datos",
        "Visualización de datos"
    ])
    if op == 1:
        ticker = prompt("Ingrese ticker a pedir")
        start_date = prompt("Ingrese fecha de inicio")
        end_date = prompt("Ingrese fecha de fin")
        get_tickers(ticker, start_date, end_date)
    elif op == 2:
        op = prompt("Indique la visualización a realizar", options=[
            "Resumen",
            "Gráfico de ticker"
        ])
        if op == 1:
            show_tickers()
        elif op == 2:
            ticker = prompt("Ingrese el ticker a graficar")
            plot_ticker(ticker)

def main():
    """
    Función principal del programa.
    """
    try:
        handle_user_input()
    except KeyboardInterrupt:
        print("\nCancelado")
    except exc.OperationError:
        print("Operación inválida")
    except Exception:
        print("Error inesperado")
        traceback.print_exc()

if __name__ == "__main__":
    main()
