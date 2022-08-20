import sqlite3

def _execute_sql_query(query, database="tickers.db"):
    con = sqlite3.connect(database)
    cur = con.cursor()
    results = cur.execute(query).fetchall()
    con.commit()
    con.close()
    return results

def insert_ticker(ticker):
    """
    Inserta un ticker en la base de datos.
    """
    db._execute_sql_query(
        """
        CREATE TABLE IF NOT EXISTS ticker (
            symbol TEXT,
            name TEXT,
            market_cap INTEGER,
            date TEXT
        )
        """
    )
    db._execute_sql_query(
        f"""
        INSERT INTO tickers VALUES (
            '{ticker["symbol"]}',
            '{ticker["name"]}',
            '{ticker["market_cap"]}',
            '{ticker["date"]}'
        )
        """
    )

def fetch_all_tickers():
    """
    Obtiene tickers de la base de datos.
    """
    db._execute_sql_query(
        """
        CREATE TABLE IF NOT EXISTS ticker (
            symbol TEXT,
            name TEXT,
            market_cap INTEGER,
            date TEXT
        )
        """
    )
    return db._execute_sql_query(
        f"""
        SELECT *
        FROM tickers
        """
    )

def fetch_stats_tickers():
    # "select symbol, min(date), max(date) from tickers group by symbol"
    """
    Obtiene las estadísticas (primera y última fecha)
    por ticker de la base de datos.
    """
    db._execute_sql_query(
        """
        CREATE TABLE IF NOT EXISTS ticker (
            symbol TEXT,
            name TEXT,
            market_cap INTEGER,
            date TEXT
        )
        """
    )
    return db._execute_sql_query(
        f"""
        SELECT
            symbol,
            MIN(date),
            MAX(date)
        FROM tickers
        GROUP BY symbol
        """
    )
