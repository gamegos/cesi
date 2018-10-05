from flask import session, jsonify
from functools import wraps
from datetime import datetime


def is_user_logged_in(log_message=""):
    def actual_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if session.get("logged_in"):
                return f(*args, **kwargs)

            if not log_message == "":
                message = log_message.format(**kwargs)
                print(message)

            return jsonify(status="error", message="Session expired"), 401

        return wrap

    return actual_decorator


def is_admin_or_normal_user(log_message=""):
    def actual_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            username = session["username"]
            usertypecode = session["usertypecode"]
            if usertypecode == 0 or usertypecode == 1:
                return f(*args, **kwargs)

            if not log_message == "":
                message = log_message.format(**kwargs)
                print("{0}: {1}".format(username, message))

            return (
                jsonify(status="error", message="You are not authorized this action"),
                403,
            )

        return wrap

    return actual_decorator


def is_admin(log_message=""):
    def actual_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            username = session["username"]
            usertypecode = session["usertypecode"]
            if usertypecode == 0:
                return f(*args, **kwargs)

            if not log_message == "":
                message = log_message.format(**kwargs)
                print("{0}: {1}".format(username, message))

            return (
                jsonify(status="error", message="You are not authorized this action"),
                403,
            )

        return wrap

    return actual_decorator
