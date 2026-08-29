import sqlite3
import bcrypt
from os import remove
import re
from utils.util_globals import *

### INITIAL DB SETUP
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


### POST
def create_post(data):
    conn = None
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO posts (owner, title, description, category_id, is_open)
            VALUES (:uid, :title, :description, :category_id, :is_open)
        """, {
            "uid": data["uid"],
            "title": data["title"],
            "description": data["description"],
            "category_id": data["category_id"],
            "is_open": data["is_open"]
        })

        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        print("create_post error:", e)
        if conn:
            conn.rollback()
            conn.close()
        return False


def update_post(data):
    conn = None
    try:
        conn = get_db()
        cur = conn.cursor()

        # Ownership check
        cur.execute("""
            SELECT owner FROM posts WHERE id = :post_id
        """, {"post_id": data["post_id"]})
        row = cur.fetchone()

        if not row or row["owner"] != data["uid"]:
            return False

        cur.execute("""
            UPDATE posts
            SET title = :title,
                description = :description,
                category_id = :category_id,
                is_open = :is_open
            WHERE id = :post_id
        """, data)

        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        print("update_post error:", e)
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
            WHERE id = :post_id AND owner = :uid
        """, {"post_id": data["post_id"], "uid": data["uid"]})

        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        print("delete_post error:", e)
        if conn:
            conn.rollback()
            conn.close()
        return False

    
def get_my_posts(uid):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT posts.id, posts.title, posts.description,
               post_category.category AS category, posts.is_open
        FROM posts
        JOIN post_category ON post_category.id = posts.category_id
        WHERE posts.owner = :uid
        ORDER BY posts.id DESC
    """, {"uid": uid})

    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


class SearchData:
    def __init__(self, uid, query):
        self.uid = uid
        self.query = query


def search_posts(data):
    """Search and rank open posts using SQLite's FTS4 index.

    Ranking happens in SQL with title, category ID, location, and description
    as descending priorities.  FTS4 performs the candidate search; no Python
    similarity calculation or sorting is used.
    """
    query = data.query.strip()
    if not query:
        return []

    conn = None
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
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
            WHERE posts.is_open = 1 AND posts.owner != :uid
            ORDER BY relevance DESC, posts.id ASC
            """
            , { "uid": data.uid, "query": query }
        )
        rows = cur.fetchall()

        return [dict(row) for row in rows]
    except Exception:
        if conn:
            conn.rollback()
            conn.close()
        return []


def search_posts_relational(search="", category="", uid=None):
    conn = get_db()
    cur = conn.cursor()

    query = """
        SELECT posts.id, posts.owner, posts.title, posts.description,
               post_category.category, posts.is_open,
               users.username, users.location
        FROM posts
        JOIN users ON posts.owner = users.id
        JOIN post_category ON post_category.id = posts.category_id
        WHERE posts.is_open = 1 AND posts.owner != :uid
    """

    params = {}

    if uid is not None:
        query += " AND posts.owner != :uid"
        params["uid"] = uid

    if category:
        query += " AND posts.category_id = :category"
        params["category"] = category

    query += " ORDER BY posts.id DESC"

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


### DB INIT
def delete_db():
    try:
        remove(DB_PATH)
        print(f"DB deleted successfully.")
    except FileNotFoundError:
        print(f"DB does not exist.")


def populate_db():
    conn = None
    try:
        conn = get_db()
        cur = conn.cursor()

        for category in DUMMY_DATA["post_category"]:
            cur.execute("INSERT INTO post_category (category) VALUES (:category)", category)
        conn.commit()

        cur.close()
        conn.close()
    except:
        if conn:
            conn.rollback()
            conn.close()

    for user in DUMMY_DATA["users"]:
        insert_user(
            user["username"],
            user["email"],
            user["password"],
            user["location"]
        )


### REGISTRATION
def encrypt_pwd(raw_pwd):
    salt = bcrypt.gensalt()
    pwd = bcrypt.hashpw(raw_pwd.encode("utf-8"), salt)
    return pwd


def check_invalid_chars(username):
    return not USERNAME_REGEX.match(username)


def user_exists_by_username(username):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def user_exists_by_email(email):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE email = ?", (email.lower(),))
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def insert_user(uname, email, pwd, loc):
    conn = get_db()
    cursor = conn.cursor()

    # might remove
    email = email.lower()
    loc = loc.lower()

    cursor.execute("""
        INSERT INTO users (username, email, password, location) VALUES (?, ?, ?, ?)
        """,
                   (uname, email, encrypt_pwd(pwd), loc))

    conn.commit()
    conn.close()


def get_pwd(uname, is_email=False):
    conn = get_db()
    cursor = conn.cursor()

    if is_email:
        cursor.execute("""
            SELECT password FROM users WHERE email = ?
            """,
            (uname,)
        )
    else:
        cursor.execute("""
            SELECT password FROM users WHERE username = ?
            """,
            (uname,)
        )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None  # no such user
    return row[0] # hashed password


def get_user_by_id(uid):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, email, location
        FROM users
        WHERE id = :uid
    """, {"uid": uid})

    user = cur.fetchone()
    conn.close()

    return user


def get_user_by_username(username):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, email, location
        FROM users
        WHERE username = :username
    """, {"username": username})

    user = cur.fetchone()
    conn.close()

    return user


def get_name(email):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username FROM users WHERE email = ?
        """,
        (email,)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None  # no such user
    return row[0] # username


def check_pwd(name, pwd):
    if '@' in name:
        name = name.lower()
        hashed = get_pwd(name, is_email=True)
    else:
        hashed = get_pwd(name)

    # User not found
    if hashed is None:
        return False

    # Compare password
    return bcrypt.checkpw(pwd.encode("utf-8"), hashed)
