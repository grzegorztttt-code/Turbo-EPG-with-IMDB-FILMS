import sqlite3

def get_conn():
    conn = sqlite3.connect("tv.db", check_same_thread=False)

    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA temp_store=MEMORY;")
    conn.execute("PRAGMA cache_size=100000;")

    return conn


def init_db():
    conn = get_conn()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS movies(
        tmdb_id INTEGER PRIMARY KEY,
        title TEXT,
        year TEXT,
        rating REAL,
        poster TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS programs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel TEXT,
        title TEXT,
        start TEXT,
        end TEXT,
        tmdb_id INTEGER
    )
    """)

    conn.commit()
