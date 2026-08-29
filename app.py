import os
from flask import Flask, g, request, session
from flask import render_template, redirect
from utils import *

app = Flask(__name__)
app.secret_key = "super-secret-key"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    name = request.form["name"]
    password = request.form["password"]

    if check_pwd(name, password):
        username = get_name(name) if '@' in name else name
        user = get_user_by_username(username)

        session["user"] = user["username"]   # username
        session["uid"]  = user["id"]         # user ID

        return redirect("/")
    else:
        return render_template("login.html", error="Invalid username or password")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    email = request.form["email"].lower()
    password = request.form["password"]
    location = request.form["location"]

    # Username taken
    if user_exists_by_username(username):
        return render_template("register.html",
                               error="Username is already taken.")

    # Email taken
    if user_exists_by_email(email):
        return render_template("register.html",
                               error="Email is already registered.")

    insert_user(username, email, password, location)
    user = get_user_by_username(username)

    session["user"] = user["username"]
    session["uid"]  = user["id"]
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.post("/post")
@app.post("/post")
def create_post_route():
    try:
        username = session["user"]
    except:
        return render_template("login.html")

    data = {
        "uid": session["uid"],
        "title": request.form["title"],
        "description": request.form["description"],
        "category_id": request.form["category_id"],
        "is_open": request.form.get("is_open", 1)
    }

    if not create_post(data):
        return "Failed to create post", 500

    return redirect("/me?created=1")


@app.route("/create-post", methods=["GET"])
def create_post_page():
    if "uid" not in session:
        return redirect("/login")

    categories = get_all_categories()
    return render_template("create_post.html", categories=categories)


@app.put("/post/<int:post_id>")
def update_post_route(post_id):
    try:
        username = session["user"]
    except:
        return render_template("login.html")

    data = {
        "uid": session["uid"],
        "post_id": post_id,
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "category_id": request.form.get("category_id"),
        "is_open": request.form.get("is_open")
    }

    if not update_post(data):
        return "Failed to update post", 500

    return "Post updated!"


@app.delete("/post/<int:post_id>")
def delete_post_route(post_id):
    try:
        username = session["user"]
    except:
        return render_template("login.html")

    data = {
        "uid": session["uid"],
        "post_id": post_id,
    }

    if not delete_post(data):
        return "Failed to delete post", 500

    return "Post deleted!"


@app.route("/discover")
def discover():
    if "uid" not in session:
        return redirect("/login")

    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    category_list = get_post_categories()

    # Use FTS search when user types something
    if search:
        data = SearchData(uid=session["uid"], query=search)
        posts = search_posts(data)
    else:
        # fallback: relational browsing
        posts = search_posts_relational(search="", category=category, uid=session["uid"])

    return render_template("discover.html",
                           posts=posts,
                           search=search,
                           category=category,
                           category_list=category_list)


@app.route("/me")
def me():
    if "uid" not in session:
        return redirect("/login")

    uid = session["uid"]

    user = get_user_by_id(uid)
    posts = get_my_posts(uid)
    categories = get_all_categories()

    return render_template("me.html", user=user, posts=posts, categories=categories)


@app.put("/api/post/<int:post_id>")
def api_update_post(post_id):
    if "uid" not in session:
        return {"ok": False, "error": "Not logged in"}, 401

    data = {
        "uid": session["uid"],
        "post_id": post_id,
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "category_id": request.form.get("category_id"),
        "is_open": 1   # <-- FIX: always keep post open
    }

    if update_post(data):
        return {"ok": True}
    else:
        return {"ok": False, "error": "Update failed"}, 500


@app.delete("/api/post/<int:post_id>")
def api_delete_post(post_id):
    if "uid" not in session:
        return {"ok": False, "error": "Not logged in"}, 401

    data = {
        "uid": session["uid"],
        "post_id": post_id
    }

    if delete_post(data):
        return {"ok": True}
    else:
        return {"ok": False, "error": "Delete failed"}, 500


delete_db()

with app.app_context():
    init_db()
    populate_db()

app.run(debug=True)