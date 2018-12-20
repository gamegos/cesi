from flask import Blueprint, jsonify, session, request, g

from decorators import is_user_logged_in, is_admin
from loggers import ActivityLog
from models import User

auth = Blueprint("auth", __name__)
activity = ActivityLog.getInstance()


@auth.route("/login/", methods=["POST"])
def login():
    data = request.get_json()
    user_credentials = {}
    invalid_fields = []
    require_fields = ["username", "password"]
    for field in require_fields:
        value = data.get(field)
        if value is None:
            invalid_fields.append(field)

        user_credentials[field] = value

    if invalid_fields:
        return (
            jsonify(
                status="error",
                message="Please enter valid value for '{}' fields".format(
                    ",".join(invalid_fields)
                ),
            ),
            400,
        )

    result = User.verify(user_credentials["username"], user_credentials["password"])
    if not result:
        session.clear()
        return jsonify(status="error", message="Invalid username/password"), 403

    session["username"] = user_credentials["username"]
    session["logged_in"] = True
    activity.logger.info("{} logged in.".format(session["username"]))
    return jsonify(status="success", message="Valid username/password")


@auth.route("/logout/", methods=["POST"])
def logout():
    username = session.get("username")
    if username is None:
        return jsonify(status="error", message="You haven't already entered"), 403

    activity.logger.error("{} logged out".format(username))
    session.clear()
    return jsonify(status="success", message="Logout")
