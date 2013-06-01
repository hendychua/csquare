from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/teacher")
def teacher_db():
    return render_template("teacher_dashboard.html")

@app.route("/student")
def student_db():
    return render_template("student_dashboard.html")

@app.route("/class")
def class_pg():
    return render_template("class_page.html")

if __name__ == "__main__":
    app.run(debug=True)