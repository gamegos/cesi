from flask import Blueprint, jsonify, session, request, g

from decorators import is_user_logged_in, is_admin
from loggers import ActivityLog
import controllers

users = Blueprint("users", __name__)
activity = ActivityLog.getInstance()


@users.route("/", methods=["GET"])
@is_user_logged_in("Illegal request for display users event.")
@is_admin(
    "Unauthorized user request for display users event. Display users event fail."
)
def user_list():
    users = controllers.get_users()
    return jsonify(status="success", users=users)


@users.route("/", methods=["POST"])
@is_user_logged_in("Illegal request for add user event.")
@is_admin("Unauthorized user for request to add user event. Add user event fail.")
def add_new_user():
    data = request.get_json()
    new_user = {}
    new_user["username"], new_user["password"] = (
        data.get("username"),
        data.get("password"),
    )
    try:
        new_user["usertype"] = int(data.get("usertype"))
    except ValueError as e:
        return jsonify(status="warning", message=str(e))

    if new_user["username"] == "" or new_user["password"] == "":
        return jsonify(status="error", message="Please enter valid value")

    try:
        controllers.add_user(
            new_user["username"], new_user["password"], new_user["usertype"]
        )
        activity.logger.error("New user added({}).".format(session["username"]))
        return jsonify(status="success", message="User added")
    except Exception as e:
        print(e)
        activity.logger.error(
            "Username is not available. Please select different username"
        )
        return jsonify(
            status="error",
            message="Username is not available. Please select different username",
        )


@users.route("/<username>/", methods=["DELETE"])
@is_user_logged_in("Illegal request for delete {username} user event.")
@is_admin("Unauthorized user for request to delete {username} user. Delete event fail.")
def delete_user(username):
    if username == "admin":
        activity.logger.error(
            "{} user request for delete admin user. Delete admin user event fail.".format(
                session["username"]
            )
        )
        return jsonify(status="error", message="Admin can't be deleted")

    controllers.delete_user(username)
    activity.logger.error("{} user deleted.".format(session["username"]))
    return jsonify(status="success")
