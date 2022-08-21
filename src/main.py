#! /usr/bin/env python3

"""
Certificación Profesional en Python (ITBA) | Trabajo Práctico Final
Alumno: Matías Huenul
"""

import traceback
from time import sleep
from datetime import datetime

import lib.plot as plot
import lib.utils as utils
import lib.database as db
import lib.exceptions as exc
import lib.polygon as polygon

def get_tickers(symbol, start_date, end_date):
    """
    Realiza una llamada a la API de Ticker y guarda
    los resultados en la base de datos.
    """
    print("Pidiendo datos...")
    tickers = []
    start = datetime.strptime(start_date, "%Y/%m/%d")
    end = datetime.strptime(end_date, "%Y/%m/%d")
    for dt in utils.get_date_range(start, end):
        date = dt.strftime("%Y-%m-%d")
        if db.fetch_all_tickers(symbol=symbol, date=date):
            print(f"Ticker {symbol} con fecha {date} ya existente "
                "en la base de datos, se omite la solicitud a la API.")
            continue
        k = 0
        max_failed_attempts = 3
        while k < max_failed_attempts:
            try:
                ticker = polygon.get_ticker(symbol, date)
                tickers.append(ticker)
                break
            except polygon.TooManyRequestsError:
                print("Se excedió el rate limit de la API - Reintentando.")
                k += 1
                sleep(k ** 3)
            except polygon.NotFoundError:
                print("No se encontró el ticker solicitado.")
                return
        if k == max_failed_attempts:
            print(
                "Se excedió el rate limit de la API, "
                "algunos resultados no pudieron ser recuperados."
            )
    for ticker in tickers:
        db.insert_ticker(ticker)
    if tickers:
        print("Datos guardados correctamente.")

def show_tickers():
    """
    Imprime un resumen de los tickers guardados en la base de datos.
    """
    print("Los tickers guardados en la base de datos son:")
    for ticker in db.fetch_stats_tickers():
        symbol = ticker["ticker"]
        min_date = ticker["min_date"]
        max_date = ticker["max_date"]
        print(f"{symbol} - {min_date} <-> {max_date}")

def plot_ticker(ticker):
    """
    Grafica los datos guardados para un ticker específico.
    """
    data = db.fetch_all_tickers(symbol=ticker)
    plot.line_plot(
        f"Visualización del ticker {ticker}",
        data,
        x="date",
        y="value",
        xlabel="Fecha",
        ylabel="Valor"
    )

def export_tickers_to_csv(filename, ticker, start_date, end_date):
    if not filename.endswith(".csv"):
        filename += ".csv"
    data = db.fetch_all_tickers(ticker=ticker, start_date=start_date, end_date=end_date)
    utils.export_to_csv(filename, data)
    print("Se exportaron los datos exitosamente.")

def handle_user_input():
    """
    Maneja el input del usuario mediante
    línea de comandos.
    """
    op = utils.prompt("Indique la operación a realizar", options=[
        "Actualización de datos",
        "Visualización de datos",
        "Exportación de datos"
    ])
    if op == 1:
        ticker = utils.prompt("Ingrese ticker a pedir")
        start_date = utils.prompt("Ingrese fecha de inicio")
        end_date = utils.prompt("Ingrese fecha de fin")
        get_tickers(ticker, start_date, end_date)
    elif op == 2:
        op = utils.prompt("Indique la visualización a realizar", options=[
            "Resumen",
            "Gráfico de ticker"
        ])
        if op == 1:
            show_tickers()
        elif op == 2:
            ticker = utils.prompt("Ingrese el ticker a graficar")
            plot_ticker(ticker)
    elif op == 3:
        filename = utils.prompt("Ingrese el nombre del archivo a generar")
        ticker = utils.prompt(
            "Ingrese ticker a exportar (o vacío para exportar todos)")
        start_date = utils.prompt(
            "Ingrese fecha de inicio a exportar "
            "(o vacío para exportar desde la primer fecha disponible)")
        end_date = utils.prompt(
            "Ingrese fecha de fin a exportar "
            "(o vacío para exportar hasta la última fecha disponible)")
        export_tickers_to_csv(filename, ticker, start_date, end_date)

def main():
    """
    Función principal del programa.
    """
    try:
        handle_user_input()
    except KeyboardInterrupt:
        print("\nCancelado.")
    except Exception:
        print("Error inesperado.")
        traceback.print_exc()

if __name__ == "__main__":
    main()
