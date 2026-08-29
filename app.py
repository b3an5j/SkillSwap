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


delete_db()

with app.app_context():
    init_db()
    populate_db()

app.run(debug=True)