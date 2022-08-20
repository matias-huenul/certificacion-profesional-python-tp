import sqlite3

def execute_sql_query(query, database="tickers.db"):
    con = sqlite3.connect(database)
    cur = con.cursor()
    results = cur.execute(query).fetchall()
    con.commit()
    con.close()
    return results
