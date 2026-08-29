import sqlite3
from pathlib import Path

DB_PATH = "database/database.sqlite"
SCHEMA_PATH = "database/schema.sql"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Read schema.sql and execute it
        with open(SCHEMA_PATH, "r") as f:
            schema = f.read()
            cursor.executescript(schema)

        conn.commit()
        conn.close()

        return True
    except Exception:
        if conn:
            conn.rollback()
            conn.close()
        return False

def insert_post(data):
    conn = None
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO posts (owner, title, description, category_id, is_open)
            VALUES (?,?,?,?,?)
        """, (data.user_id, data.title, data.description, data.category_id, data.is_open))
        conn.commit()

        # Print something

        cur.close()
        conn.close()

        return True
    except Exception:
        if conn:
            conn.rollback()
            conn.close()
        return False

def update_post(data):
    conn = None
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            UPDATE posts
            SET
                title = ?,
                description = ?,
                category_id = ?,
                is_open = ?
            WHERE owner = ? AND id = ?
        """, (data.title, data.description, data.category_id, data.is_open, data.user_id, data.post_id))
        conn.commit()

        # Print something

        cur.close()
        conn.close()

        return True
    except Exception:
        if conn:
            conn.rollback()
            conn.close()
        return False

def delete_post(data):
    conn = None
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM posts
            WHERE owner = ? AND id = ?
        """, (data.user_id, data.post_id))
        conn.commit()

        # Print something

        cur.close()
        conn.close()

        return True
    except Exception:
        if conn:
            conn.rollback()
            conn.close()
        return False
