from flask import (
    session,
    jsonify
)
from functools import wraps

def is_user_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get('logged_in'):
            return f(*args, **kwargs)
        else:
            return jsonify(message='Session expired'), 403

    return wrap