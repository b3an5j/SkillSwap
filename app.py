import os
from flask import Flask, g, request, session
from database.db_utils import *

app = Flask(__name__)

# Initialize DB on startup
with app.app_context():
    init_db()

# Create DB if missing
if not os.path.exists(DB_PATH):
    print("Database not found. Creating new database...")
    init_db()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"