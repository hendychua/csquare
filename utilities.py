from functools import wraps

from flask import session
from flask import url_for
from flask import request
from flask import redirect
from flask import g

SESSION_LOGIN_USERNAME = "session_login_username"
SESSION_LOGIN_USERTYPE = "session_login_usertype"
SESSION_LOGIN_USERID = "session_login_userid"

def login_required(func):
    """
    A wrapper function for ensuring that user is loggedin when
    accessing pages that require them to do so.
    Usage: put @login_required before method declaration.
    """
    
    @wraps(func)
    def check_login(*args, **kwargs):
        if session.get(SESSION_LOGIN_USERID, None) is None:
            return redirect(url_for("index"))

        g.userid = session.get(SESSION_LOGIN_USERID)
        g.usertype = session.get(SESSION_LOGIN_USERTYPE)
        g.username = session.get(SESSION_LOGIN_USERNAME)
        return func(*args, **kwargs)

    return check_login