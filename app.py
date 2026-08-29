import os
from flask import Flask, g, request, session, render_template
from utils import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    name = request.form["name"]
    password = request.form["password"]

    # check_user(name, "")
    
    return "Logged in!"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    location = request.form["location"]

    insert_user(
        username,
        email,
        password,
        location
    )

    return "Registered!"


delete_db()

with app.app_context():
    init_db()
    populate_db()

app.run(debug=True)