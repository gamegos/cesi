from flask import Blueprint, jsonify, request, g

from decorators import is_user_logged_in
from loggers import ActivityLog
import controllers
from models import User

profile = Blueprint("profile", __name__)
activity = ActivityLog.getInstance()


@profile.route("/", methods=["GET"])
@is_user_logged_in("Illegal request to get your own information")
def get_own_info():
    user = controllers.get_user(g.user.username)
    print(user)
    return jsonify(status="success", user=user)


@profile.route("/password/", methods=["PUT"])
@is_user_logged_in("Illegal request to change your own password.")
def change_own_password():
    username = g.user.username
    data = request.get_json()
    old_password = data.get("oldPassword")
    new_password = data.get("newPassword")
    if old_password == "" or new_password == "":
        return (
            jsonify(
                status="error",
                message="Please enter valid value old password or new_password",
            ),
            400,
        )

    result = User.verify(username, old_password)
    if not result:
        activity.logger.error(
            "Old password is wrong to change {} 's password.".format(username)
        )
        return jsonify(status="error", message="Old password is wrong"), 400

    User.update_password(username, new_password)
    activity.logger.error("{} user changed the own password.".format(username))
    return jsonify(status="success")
