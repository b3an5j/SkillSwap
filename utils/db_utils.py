import sqlite3
import bcrypt
from pathlib import Path
from os import remove

DB_PATH = "database/database.sqlite"
SCHEMA_PATH = "database/schema.sql"
DUMMY_DATA = [{
  "username": "cplomer0",
  "email": "gtrimnell0@people.com.cn",
  "password": "gcrannach0",
  "location": "Philippines"
}, {
  "username": "ltamas1",
  "email": "rruilton1@tumblr.com",
  "password": "apitson1",
  "location": "Azerbaijan"
}, {
  "username": "csmallacombe2",
  "email": "jcumbridge2@stanford.edu",
  "password": "jdows2",
  "location": "Japan"
}, {
  "username": "smoncrieffe3",
  "email": "vmcgairl3@github.io",
  "password": "jkefford3",
  "location": "Indonesia"
}, {
  "username": "cjeffries4",
  "email": "jsweet4@uiuc.edu",
  "password": "bvaisey4",
  "location": "South Africa"
}, {
  "username": "jbardell5",
  "email": "kellerman5@sbwire.com",
  "password": "msanbrook5",
  "location": "Democratic Republic of the Congo"
}, {
  "username": "kkrzysztofiak6",
  "email": "lsoutherton6@symantec.com",
  "password": "bechallier6",
  "location": "Argentina"
}, {
  "username": "kbinestead7",
  "email": "ccorkan7@oracle.com",
  "password": "lmccaig7",
  "location": "Brazil"
}, {
  "username": "lhaskey8",
  "email": "sdonoghue8@posterous.com",
  "password": "hmcnicol8",
  "location": "China"
}, {
  "username": "rsetter9",
  "email": "khickenbottom9@unesco.org",
  "password": "wfilinkov9",
  "location": "Indonesia"
}]

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

def delete_db():
    try:
        remove(DB_PATH)
        print(f"DB deleted successfully.")
    except FileNotFoundError:
        print(f"DB does not exist.")


def populate_db():
    for user in DUMMY_DATA:
        insert_user(
            user["username"],
            user["email"],
            user["password"],
            user["location"]
        )


def encrypt_pwd(raw_pwd):
    salt = bcrypt.gensalt()
    pwd = str(bcrypt.hashpw(raw_pwd.encode("utf-8"), salt))
    return pwd


def insert_user(uname, email, pwd, loc):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, email, password, location) VALUES (?, ?, ?, ?)",
                   (uname, email, encrypt_pwd(pwd), loc))

    conn.commit()
    conn.close()


# def check_user(uname, pwd):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM users WHERE username = ?", (uname,))

#     for row in cursor.fetchall():
#         for data in row:
#             print(data)

    
    

    conn.commit()
    conn.close()