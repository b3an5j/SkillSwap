import sqlite3
from pathlib import Path

DB_PATH = "database/database.sqlite"
SCHEMA_PATH = "database/schema.sql"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Read schema.sql and execute it
    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()
        cursor.executescript(schema)

    conn.commit()
    conn.close()
