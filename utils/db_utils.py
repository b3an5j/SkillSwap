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

def search_posts(query, connection=None):
    """Search and rank open posts using SQLite's FTS4 index.

    Ranking happens in SQL with title, category ID, location, and description
    as descending priorities.  FTS4 performs the candidate search; no Python
    similarity calculation or sorting is used.
    """
    if not isinstance(query, str):
        raise TypeError("query must be a string")

    query = query.strip()
    if not query:
        return []

    owns_connection = connection is None
    conn = connection or get_db()
    try:
        rows = conn.execute(
            """
            WITH title_matches AS (
                SELECT docid
                FROM posts_search
                WHERE posts_search MATCH
                    ('title:' || replace(:query, ' ', ' title:'))
            ),
            category_matches AS (
                SELECT docid
                FROM posts_search
                WHERE posts_search MATCH
                    ('category:' || replace(:query, ' ', ' category:'))
            ),
            location_matches AS (
                SELECT docid
                FROM posts_search
                WHERE posts_search MATCH
                    ('location:' || replace(:query, ' ', ' location:'))
            ),
            description_matches AS (
                SELECT docid
                FROM posts_search
                WHERE posts_search MATCH
                    ('description:' || replace(:query, ' ', ' description:'))
            ),
            matching_posts AS (
                SELECT docid FROM title_matches
                UNION SELECT docid FROM category_matches
                UNION SELECT docid FROM location_matches
                UNION SELECT docid FROM description_matches
            )
            SELECT posts.id, posts.owner, posts.title, posts.description,
                   post_category.category, posts.is_open, users.username,
                   users.location,
                   (CASE WHEN posts.id IN (SELECT docid FROM title_matches)
                         THEN 1000 ELSE 0 END
                    + CASE WHEN posts.id IN (SELECT docid FROM category_matches)
                           THEN 100 ELSE 0 END
                    + CASE WHEN posts.id IN (SELECT docid FROM location_matches)
                           THEN 10 ELSE 0 END
                    + CASE WHEN posts.id IN (SELECT docid FROM description_matches)
                           THEN 1 ELSE 0 END) AS relevance
            FROM matching_posts
            JOIN post_category ON post_category.id = posts.category_id
            JOIN posts ON posts.id = matching_posts.docid
            JOIN users ON users.id = posts.owner
            WHERE posts.is_open = 1
            ORDER BY relevance DESC, posts.id ASC
            """
            , {"query": query}
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        if owns_connection:
            conn.close()

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

#     conn.commit()
#     conn.close()
