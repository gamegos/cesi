from flask import session, jsonify, g
from functools import wraps
from datetime import datetime

from models import User


def is_user_logged_in(log_message=""):
    def actual_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if session.get("logged_in"):
                g.username = session["username"]
                g.user = User.query.filter_by(
                    username=session["username"]
                ).first_or_404()
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
            if g.user.is_admin and g.user.is_normal_user:
                return f(*args, **kwargs)

            if not log_message == "":
                message = log_message.format(**kwargs)
                print("{0}: {1}".format(g.username, message))

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
            if g.user.is_admin:
                return f(*args, **kwargs)

            if not log_message == "":
                message = log_message.format(**kwargs)
                print("{0}: {1}".format(g.username, message))

            return (
                jsonify(status="error", message="You are not authorized this action"),
                403,
            )

        return wrap

    return actual_decorator
