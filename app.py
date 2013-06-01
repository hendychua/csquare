from flask import Flask
from flask import render_template
import sqlite3

PARSE_APP_ID = "Ag4XfW4UyetRRHaphILYG6b95cBCOxjdGWOEwjXz"
PARSE_REST_API_KEY = "BI1PVdG16Es2G4t0w2HQGsTnAkNrhRmFJaXgIGLv"

DEBUG_MODE = True
PORT = 5000
HOST = '127.0.0.1'

app = Flask(__name__)
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route("/")
def index():
    return "index"
    
@app.route("/admin")
def admin():
    return "admin dashboard"
    
@app.route("/participant")
def participant():
    return "participant dashboard"
    
@app.route("/classes")
def admin_classes():
    return "admin classes"

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG_MODE)