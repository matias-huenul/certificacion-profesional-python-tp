import csv
import json
from datetime import datetime
from datetime import timedelta

def get_date_range(start_date, end_date, fmt="%Y-%m-%d"):
    """
    Devuelve las fechas en el intervalo [start_date, end_date].
    """
    start = datetime.strptime(start_date, fmt)
    end = datetime.strptime(end_date, fmt)
    dates = []
    for i in range((end - start).days + 1):
        date = start + timedelta(days=i)
        dates.append(date.strftime(fmt))
    return dates

def prompt(message, options=[], validate_date=False):
    """
    Recibe input del usuario, el cual puede
    ser un texto o un valor dentro de posibles opciones.
    """
    message += ":\n"
    for i, option in enumerate(options):
        message += f"  {i + 1}. {option}\n"
    response = input(message + "> ")
    if not options:
        if validate_date:
            while True:
                try:
                    datetime.strptime(response, "%Y-%m-%d")
                    break
                except ValueError:
                    response = input("Fecha inválida.\n> ")
        return response
    while True:
        try:
            response = int(response)
        except ValueError:
            response = -1
        if response < 0 or response > len(options):
            response = input("Opción inválida.\n> ")
        else:
            break
    return response

def export_to_csv(filename, data):
    """
    Exporta datos a un archivo en formato csv.
    """
    with open(filename, "w") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        for item in data:
            writer.writerow(item)

def export_to_json(filename, data):
    """
    Exporta datos a un archivo en formato json.
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def print_as_table(data_list):
    """
    Imprime datos en forma de tabla.
    """
    max_len = {}
    for data in data_list:
        for key, value in data.items():
            max_len[key] = max(max_len.get(key, 0), len(str(key)))
            max_len[key] = max(max_len.get(key, 0), len(str(value)))
    for key in data_list[0].keys():
        print(f"{key}" + ((max_len[key] - len(str(key)) + 2) * " "), end="")
    print()
    for key in data_list[0].keys():
        print((max_len[key] * "-" + "  "), end="")
    print()
    for data in data_list:
        for key, value in data.items():
            print(
                f"{value}" + ((max_len[key] - len(str(value)) + 2) * " "),
                end=""
            )
        print()
