from datetime import timedelta

def get_date_range(start_date, end_date):
    dates = []
    for i in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=i)
        dates.append(date)
    return dates
