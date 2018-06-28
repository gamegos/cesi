from flask import (
    session,
    jsonify
)
from functools import wraps
from datetime import datetime

from loggers import ActivityLog

def is_user_logged_in(log_message=""):
    def actual_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            activity = ActivityLog.getInstance()
            if session.get('logged_in'):
                return f(*args, **kwargs)

            if not log_message == "":
                message = log_message.format(**kwargs)
                activity.logger.error(message)

            return jsonify(message='Session expired'), 403

        return wrap

    return actual_decorator

def is_admin_or_normal_user(log_message=""):
    def actual_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            activity = ActivityLog.getInstance()
            username = session['username']
            usertypecode = session['usertypecode']
            if usertypecode == 0 or usertypecode == 1:
                return f(*args, **kwargs)

            if not log_message == "":
                message = log_message.format(**kwargs)
                activity.logger.error(f"{username}: {message}")

            return jsonify(message='You are not authorized this action'), 403

        return wrap

    return actual_decorator

def is_admin(log_message=""):
    def actual_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            activity = ActivityLog.getInstance()
            username = session['username']
            usertypecode = session['usertypecode']
            if usertypecode == 0:
                return f(*args, **kwargs)

            if not log_message == "":
                message = log_message.format(**kwargs)
                activity.logger.error(f"{username}: {message}")

            return jsonify(message='You are not authorized this action'), 403

        return wrap

    return actual_decorator