#! /usr/bin/env python3

class OperationError(Exception):
    """
    Excepción a ser lanzada ante un código de
    operación inválido.
    """
    pass

def make_api_request(ticker, start_date, end_date):
    """
    Realiza una llamada a la API de Ticker y devuelve
    el resultado.
    """
    return {}

def save_data_to_db(data):
    """
    Persiste información de tickers en la base
    de datos.
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
            raise OperationError
    else:
        raise OperationError

def main():
    """
    Función principal del programa.
    """
    try:
        handle_user_input()
    except KeyboardInterrupt:
        print("\nCancelado")
    except OperationError:
        print("Operación inválida")
    except Exception:
        print("Error inesperado")

if __name__ == "__main__":
    main()
