from utilities import login_required
from utilities import SESSION_LOGIN_ID
from utilities import SESSION_LOGIN_USERTYPE
from parse_keys import PARSE_APP_ID, PARSE_REST_API_KEY, PARSE_API_URL

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import g
import requests

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

@app.route("/")
def index():
    if session.get(SESSION_LOGIN_ID, None) is None:
        return render_template("index.html")
    else:
        return redirect("/dashboard")
        
@app.route("/about")
def about_us():
    return render_template("index.html")

@app.route("/login", methods=["get", "post"])
def login_validation():
    headers = {"X-Parse-Application-Id": PARSE_APP_ID, "X-Parse-REST-API-Key": PARSE_REST_API_KEY}
    url = PARSE_API_URL + "/login"
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    params = dict(username=username, password=password)
    r = requests.get(url, params=params, headers=headers)
    res = r.json()
    if "code" in res.keys() and res['code'] == 101: ##authentication failed
        return redirect("/")
    else:
        if session.get(SESSION_LOGIN_ID, None) is None:
            session[SESSION_LOGIN_ID] = res['username']
            usertypeId = res['user_type']['objectId']
            url = PARSE_API_URL + "/classes/user_type" + "/" + usertypeId
            r = requests.get(url, headers=headers)
            session[SESSION_LOGIN_USERTYPE] = r.json()['type']
            return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.pop(SESSION_LOGIN_ID, None)
    session.pop(SESSION_LOGIN_USERTYPE, None)
    return redirect("/")            

@app.route("/dashboard")
@login_required
def dashboard():
        if g.usertype == "student":
            return "stu"
        elif g.usertype == "class_admin":
            #get classes under this admin
            #determine top 3 classes with most recent activities
                #get these classes number of students
                #get number of assignments
                #get 2 latest assignments completion rate
                #get 3 latest student activities in this class
            return render_template("teacher_dashboard.html")

@app.route("/assignment/create")
@login_required
def create_assignment():
    if g.usertype == "student":
        return "Oops you do not have permission to view this page"
        
    elif g.usertype == "class_admin":
        return "Page to allow teachers to create assignments"

@app.route("/assignment/<objectId>")
@login_required
def assignment(objectId):
    if g.usertype == "student":
        # student will have the option to submit the assignment after completion
        #if assignment completed, student views his results
        return "View an assignment in detail"

    elif g.usertype == "class_admin":
        # admin views the assignment
        # shows details such as completion rate, who has not completed it
        # avg score, score rankings
        return "View an assignment in detail"
        
@app.route("/class/create")
@login_required
def create_class():
    if g.usertype == "student":
        return "Oops you do not have permission to view this page"

    elif g.usertype == "class_admin":
        return "Page to allow teachers to create classes"
        
@app.route("/assignment/<objectId>")
@login_required
def classes(objectId):
    if g.usertype == "student":
        # students will view class performance (by subjects)
        # where they stand
        # storyline
        # and progress to goal
        return "View an assignment in detail"

    elif g.usertype == "class_admin":
        # admins will view class performance (by subjects)
        # where they stand
        # storyline
        # and progress to goal
        return "View an assignment in detail"

if __name__ == "__main__":
    app.run()
