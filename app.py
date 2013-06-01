from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/teacher")
def teacher_db():
    return render_template("teacher_dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)