import json

from utilities import login_required
from utilities import SESSION_LOGIN_USERNAME
from utilities import SESSION_LOGIN_USERTYPE
from utilities import SESSION_LOGIN_USERID
from parse_keys import PARSE_APP_ID, PARSE_REST_API_KEY, PARSE_API_URL, PARSE_HEADERS

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
    if session.get(SESSION_LOGIN_USERID, None) is None:
        return render_template("index.html")
    else:
        return redirect("/dashboard")
        
@app.route("/about")
def about_us():
    return render_template("index.html")

@app.route("/login", methods=["get", "post"])
def login_validation():
    headers = PARSE_HEADERS
    url = PARSE_API_URL + "/login"
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    params = dict(username=username, password=password)
    r = requests.get(url, params=params, headers=headers)
    res = r.json()
    if "code" in res.keys() and res['code'] == 101: ##authentication failed
        return redirect("/")
    else:
        if session.get(SESSION_LOGIN_USERID, None) is None:
            usertypeId = res['user_type']['objectId']
            url = PARSE_API_URL + "/classes/user_type" + "/" + usertypeId
            r = requests.get(url, headers=headers)
            session[SESSION_LOGIN_USERNAME] = res['username']
            session[SESSION_LOGIN_USERID] = res['objectId']
            session[SESSION_LOGIN_USERTYPE] = r.json()['type']
            return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.pop(SESSION_LOGIN_USERNAME, None)
    session.pop(SESSION_LOGIN_USERTYPE, None)
    session.pop(SESSION_LOGIN_USERID, None) 
    return redirect("/")            

@app.route("/dashboard")
@login_required
def dashboard():
        if g.usertype == "student":
            return "stu"
        elif g.usertype == "class_admin":
                #get 3 latest student activities in this class
                
            url = PARSE_API_URL + "/classes/classes_admin_assoc"
            params = dict(where=json.dumps(dict(admin_id={
                     "__type": "Pointer",
                     "className": "_User",
                     "objectId": g.userid
                   })))
            r = requests.get(url, params=params, headers=PARSE_HEADERS)
            
            classes = []
            for c in r.json()['results']:
                url = PARSE_API_URL + "/classes/classes" + "/" + c['class_id']['objectId']
                r = requests.get(url, headers=PARSE_HEADERS)
                classes.append(r.json())
            
            class_subjects = []    
            for c in classes:
                url = PARSE_API_URL + "/classes/subject" + "/" + c['subject_id']['objectId']
                r = requests.get(url, headers=PARSE_HEADERS)
                class_subjects.append(r.json()['subject_title'])
                
            top_classes_student_count = []
            top_classes_assignments = []
            i = 0
            for c in classes:
                if i == 3:
                    break
                c = classes[i]
                url = PARSE_API_URL + "/classes/classes_student_assoc"
                params = dict(where=json.dumps(dict(class_id={
                         "__type": "Pointer",
                         "className": "classes",
                         "objectId": c['objectId']
                       })), count=1, limit=0)
                r = requests.get(url, params=params, headers=PARSE_HEADERS)
                top_classes_student_count.append(r.json()['count'])
                
                url = PARSE_API_URL + "/classes/assignment_class_assoc"
                params = dict(where=json.dumps(dict(class_id={
                         "__type": "Pointer",
                         "className": "classes",
                         "objectId": c['objectId']
                       })))
                r = requests.get(url, params=params, headers=PARSE_HEADERS)
                top_classes_assignments.append(r.json()['results'])
                
                i+=1
            
            i=0
            top_classes_assignments_completion_ratio = []
            for assignment_list in top_classes_assignments:
                ratio_list = []
                for assignment in assignment_list:
                    if i==2:
                        break
                    url = PARSE_API_URL + "/classes/assignment_student_assoc"
                    params = dict(where=json.dumps(dict(assignment_id={
                             "__type": "Pointer",
                             "className": "assignments",
                             "objectId": assignment['assignment_id']
                           })))
                    r = requests.get(url, params=params, headers=PARSE_HEADERS)
                    students_assigned = len(r.json()['results'])
                    students_completed = 0
                    for row in r.json()['results']:
                        if row['assignment_status'] == "done":
                            students_completed += 1
                    completed_assigned_ratio = (students_completed, students_assigned)
                    ratio_list.append(completed_assigned_ratio)
                    i+=1

                top_classes_assignments_completion_ratio.append(ratio_list)
                
            g.classes = classes
            g.class_subjects = class_subjects
            g.top_classes_student_count = top_classes_student_count
            g.top_classes_assignments = top_classes_assignments
            g.top_classes_assignments_completion_ratio = top_classes_assignments_completion_ratio
            print g.classes
            print g.class_subjects
            print g.top_classes_student_count
            print g.top_classes_assignments
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
