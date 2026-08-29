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
        session["user"] = get_name(name) if '@' in name else name
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
    session["user"] = username
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.post("/post")
def create_post_route():
    data = {
        "user_id": request.form["user_id"],
        "title": request.form["title"],
        "description": request.form["description"],
        "category_id": request.form["category_id"],
        "is_open": request.form.get("is_open", 1)
    }

    if not create_post(data):
        return "Failed to create post", 500

    return "Post created!", 201


@app.put("/post/<int:post_id>")
def update_post_route(post_id):
    data = {
        "user_id": request.form["user_id"],
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
    data = {
        "user_id": request.form["user_id"],
        "post_id": post_id,
    }

    if not delete_post(data):
        return "Failed to delete post", 500

    return "Post deleted!"


delete_db()

with app.app_context():
    init_db()
    populate_db()

app.run(debug=True)