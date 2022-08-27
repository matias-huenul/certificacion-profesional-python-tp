#! /usr/bin/env python3

"""
Certificación Profesional en Python (ITBA) | Trabajo Práctico Final
Alumno: Matías Huenul
"""

import lib.plot as plot
import lib.utils as utils
import lib.database as db
import lib.polygon as polygon
from time import sleep

def get_tickers(symbol, start_date, end_date):
    """
    Realiza una llamada a la API de Ticker y guarda
    los resultados en la base de datos.
    """
    print("Pidiendo datos...")
    tickers = []
    for date in utils.get_date_range(start_date, end_date):
        if db.fetch_all_tickers(symbol=symbol, date=date):
            print(f"Ticker {symbol} con fecha {date} ya existente "
                "en la base de datos, se omite la solicitud a la API.")
            continue
        k = 0
        max_failed_attempts = 3
        while k < max_failed_attempts:
            try:
                ticker = polygon.get_ticker(symbol, date)
                if ticker:
                    tickers.append(ticker)
                break
            except polygon.APIKeyNotFoundError:
                print("No se especificó la API key de Polygon.")
                return
            except polygon.NotFoundError:
                print("No se encontró el ticker solicitado.")
                return
            except polygon.TooManyRequestsError:
                print("Se excedió el rate limit de la API, reintentando.")
                k += 1
                sleep(2 ** (k + 1))
        if k == max_failed_attempts:
            print(
                "Se excedió el rate limit de la API, "
                "algunos resultados no pudieron ser recuperados."
            )
    for ticker in tickers:
        db.insert_ticker(ticker)
    if tickers:
        print("Datos guardados correctamente.")
    else:
        print("No hay datos nuevos a guardar.")

def show_tickers():
    """
    Imprime un resumen de los tickers guardados en la base de datos.
    """
    tickers = db.fetch_stats_tickers()
    if not tickers:
        print("No hay información en la base de datos.")
        return
    print("Los tickers guardados en la base de datos son:")
    utils.print_as_table(tickers)

def plot_ticker(ticker):
    """
    Grafica los datos guardados para un ticker específico.
    """
    data = db.fetch_all_tickers(symbol=ticker)
    if not data:
        print("No se encontraron datos para el ticker solicitado.")
        return
    plot.line_plot(
        f"Visualización del ticker {ticker}",
        data,
        x="date",
        y="value",
        xlabel="Fecha",
        ylabel="Valor"
    )

def export_tickers_to_file(filename, symbol, start_date, end_date, file_format):
    """
    Exporta la información almacenada en la base de datos
    a un archivo en formato csv o json.
    """
    if not filename.endswith(f".{file_format}"):
        filename += f".{file_format}"
    data = db.fetch_all_tickers(symbol=symbol, start_date=start_date, end_date=end_date)
    if file_format == "csv":
        utils.export_to_csv(filename, data)
    elif file_format == "json":
        utils.export_to_json(filename, data)
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
        file_format = utils.prompt(
            "Ingrese el formato de exportación",
            options=["csv", "json"]
        )
        filename = utils.prompt("Ingrese el nombre del archivo a generar")
        symbol = utils.prompt(
            "Ingrese ticker a exportar (o vacío para exportar todos)")
        start_date = utils.prompt(
            "Ingrese fecha de inicio a exportar "
            "(o vacío para exportar desde la primer fecha disponible)")
        end_date = utils.prompt(
            "Ingrese fecha de fin a exportar "
            "(o vacío para exportar hasta la última fecha disponible)")
        export_tickers_to_file(
            filename,
            symbol,
            start_date,
            end_date,
            file_format="csv" if file_format == 1 else "json"
        )
    
    op = utils.prompt("¿Desea realizar otra operación?", options=["Sí", "No"])
    if op == 1:
        handle_user_input()

def main():
    """
    Función principal del programa.
    """
    try:
        handle_user_input()
    except KeyboardInterrupt:
        print("\nCancelado.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
