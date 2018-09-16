from flask import Blueprint, jsonify, session, request, g

from decorators import is_user_logged_in, is_admin
from loggers import ActivityLog
import controllers

auth = Blueprint("auth", __name__)
activity = ActivityLog.getInstance()


@auth.route("/login/", methods=["POST"])
def login():
    data = request.get_json()
    req_username, req_password = data.get("username"), data.get("password")
    result = controllers.validate_user(req_username, req_password)
    if not result:
        session.clear()
        return jsonify(status="error", message="Invalid username/password")

    username, _, usertype = result[0]
    session["username"] = username
    session["logged_in"] = True
    session["usertypecode"] = usertype
    activity.logger.info("{} logged in.".format(session["username"]))
    return jsonify(status="success", message="Valid username/password")


@auth.route("/logout/", methods=["POST"])
def logout():
    username = session.get("username")
    if username is None:
        return jsonify(status="error", message="You haven't already entered")

    activity.logger.error("{} logged out".format(username))
    session.clear()
    return jsonify(status="success", message="Logout")
