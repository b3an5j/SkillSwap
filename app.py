import os
from flask import Flask, g, request, session, render_template
from utils import *

app = Flask(__name__)

# Initialize DB on startup
with app.app_context():
    init_db()

# Create DB if missing
if not os.path.exists(DB_PATH):
    print("Database not found. Creating new database...")
    init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"]
    password = request.form["password"]

    # TODO: check DB for user
    

    # TODO: verify password hash
    return "Logged in!"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    # TODO: insert into DB
    # TODO: hash password

    return "Registered!"
