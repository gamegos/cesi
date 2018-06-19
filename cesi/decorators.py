from flask import (
    session,
    jsonify
)
from functools import wraps
from datetime import datetime

def is_user_logged_in(log_message=""):
    def actual_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if session.get('logged_in'):
                return f(*args, **kwargs)
            else:
                if not log_message == "":
                    message = log_message.format(**kwargs)
                    print(message)
                    #add_log = open(ACTIVITY_LOG, "a")
                    #add_log.write("{} - {}\n".format(datetime.now().ctime(), message))
                return jsonify(message='Session expired'), 403

        return wrap

    return actual_decorator

def is_admin_or_normal_user(log_message=""):
    def actual_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            usertype = session['usertype']
            if usertype == 0 or usertype == 1:
                return f(*args, **kwargs)
            else:
                if not log_message == "":
                    kwargs.update({'user': session['username']})
                    message = log_message.format(**kwargs)
                    print(message)
                return jsonify(message='You are not authorized this action'), 403

        return wrap

    return actual_decorator

def is_admin(log_message=""):
    def actual_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            usertype = session['usertype']
            if usertype == 0:
                return f(*args, **kwargs)
            else:
                if not log_message == "":
                    kwargs.update({'user': session['username']})
                    message = log_message.format(**kwargs)
                    print(message)
                return jsonify(message='You are not authorized this action'), 403

        return wrap

    return actual_decorator