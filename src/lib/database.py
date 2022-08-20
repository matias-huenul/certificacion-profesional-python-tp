import sqlite3

def _execute_sql_query(query, database="tickers.db"):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tickers (
            symbol TEXT,
            name TEXT,
            value INTEGER,
            date TEXT
        )
        """
    )
    print(query)
    results = cur.execute(query).fetchall()
    con.commit()
    con.close()
    return results

def insert_ticker(ticker):
    """
    Inserta un ticker en la base de datos.
    """
    _execute_sql_query(
        f"""
        INSERT INTO tickers VALUES (
            '{ticker["symbol"]}',
            '{ticker["name"]}',
            '{ticker["value"]}',
            '{ticker["date"]}'
        )
        """
    )

def fetch_all_tickers(**filters):
    """
    Obtiene tickers de la base de datos.
    """
    where_clause = "" if not filters else "WHERE "
    for key, value in filters.items():
        where_clause += f"{key} = '{value}' AND "
    where_clause = where_clause.rstrip(" AND ")
    rows = _execute_sql_query(
        f"""
        SELECT *
        FROM tickers
        {where_clause}
        """
    )
    row_to_dict = lambda row: {
        "ticker": row[0],
        "name": row[1],
        "value": row[2],
        "date": row[3]
    }
    return [row_to_dict(row) for row in rows]

def fetch_stats_tickers():
    """
    Obtiene las estadísticas (primera y última fecha)
    por ticker de la base de datos.
    """
    rows = _execute_sql_query(
        f"""
        SELECT
            symbol,
            MIN(date),
            MAX(date)
        FROM tickers
        GROUP BY symbol
        """
    )
    row_to_dict = lambda row: {
        "ticker": row[0],
        "min_date": row[1],
        "max_date": row[2]
    }
    return [row_to_dict(row) for row in rows]
