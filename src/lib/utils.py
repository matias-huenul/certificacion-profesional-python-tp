def get_date_range(start_date, end_date):
    dates = []
    for i in range((end - start).days + 1):
        date = start + timedelta(days=i)
        dates.append(date)
    return dates
