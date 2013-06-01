from functools import wraps

from flask import session
from flask import url_for
from flask import request
from flask import redirect
from flask import g

SESSION_LOGIN_ID = "session_login_id"
SESSION_LOGIN_USERTYPE = "session_login_usertype"

def login_required(func):
    """
    A wrapper function for ensuring that user is loggedin when
    accessing pages that require them to do so.
    Usage: put @login_required before method declaration.
    """
    
    @wraps(func)
    def check_login(*args, **kwargs):
        if session.get(SESSION_LOGIN_ID, None) is None:
            return redirect(url_for("index"))

        g.userid = session.get(SESSION_LOGIN_ID)
        g.usertype = session.get(SESSION_LOGIN_USERTYPE)
        return func(*args, **kwargs)

    return check_login