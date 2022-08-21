import csv
import json
from datetime import datetime
from datetime import timedelta

def get_date_range(start_date, end_date, fmt="%Y-%m-%d"):
    start = datetime.strptime(start_date, fmt)
    end = datetime.strptime(end_date, fmt)
    dates = []
    for i in range((end - start).days + 1):
        date = start + timedelta(days=i)
        dates.append(date.strftime(fmt))
    return dates

def prompt(message, options=[]):
    """
    Recibe input del usuario, el cual puede
    ser un texto o un valor dentro de posibles opciones.
    """
    message += ":\n"
    for i, option in enumerate(options):
        message += f"  {i + 1}. {option}\n"
    response = input(message + "> ")
    if not options:
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
    with open(filename, "w") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        for item in data:
            writer.writerow(item)

def export_to_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
