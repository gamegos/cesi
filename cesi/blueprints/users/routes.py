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
    invalid_fields = []
    require_fields = ["username", "password", "usertype"]
    for field in require_fields:
        value = data.get(field)
        if value is None:
            invalid_fields.append(field)

        new_user[field] = value

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

    try:
        new_user["usertype"] = int(new_user["usertype"])
    except (ValueError, TypeError) as e:
        return jsonify(status="error", message=str(e)), 400

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
        return (
            jsonify(
                status="error",
                message="Username is not available. Please select different username",
            ),
            400,
        )


@users.route("/<username>/", methods=["DELETE"])
@is_user_logged_in("Illegal request for delete {username} user event.")
@is_admin("Unauthorized user for request to delete {username} user. Delete event fail.")
def delete_user(username):
    if username == "admin":
        activity.logger.error(
            "'{}' user request for delete 'admin' user. Delete 'admin' user event fail.".format(
                session["username"]
            )
        )
        return jsonify(status="error", message="Admin can't be deleted"), 403

    controllers.delete_user(username)
    activity.logger.error(
        "'{}' user deleted by '{}' user.".format(username, session["username"])
    )
    return jsonify(status="success")
