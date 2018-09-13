from flask import (
    Blueprint,
    jsonify,
    session,
    request,
    g
)

from decorators import (
    is_user_logged_in,
    is_admin
)
from loggers import ActivityLog
import controllers

users = Blueprint('users', __name__)
activity = ActivityLog.getInstance()

@users.route('/', methods=['GET'])
@is_user_logged_in("Illegal request for display users event.")
@is_admin("Unauthorized user request for display users event. Display users event fail.")
def user_list():
    users = controllers.get_users()
    return jsonify(status='success', users=users)

@users.route('/<username>/delete/', methods=["DELETE"])
@is_user_logged_in("Illegal request for delete {username} user event.")
@is_admin("Unauthorized user for request to delete {username} user. Delete event fail.")
def delete_user(username):
    if username == "admin":
        activity.logger.error("{} user request for delete admin user. Delete admin user event fail.".format(session['username']))
        return jsonify(status="error", message="Admin can't be deleted")

    controllers.delete_user(username)
    activity.logger.error("{} user deleted.".format(session['username']))
    return jsonify(status="success")

# Writes new user information to database
@users.route('/add/', methods = ['POST'])
@is_user_logged_in("Illegal request for add user event.")
@is_admin("Unauthorized user for request to add user event. Add user event fail.")
def adduserhandler():
    data = request.get_json()
    new_user = {}
    new_user['username'], new_user['password'] = data.get('username'), data.get('password')
    new_user['confirm_password'] = data.get('confirmpassword')
    try:
        new_user['usertype'] = int(data.get('usertype'))
    except ValueError as e:
        return jsonify(status="warning", message=str(e))

    if new_user['username'] == "" or new_user['password'] == "" or new_user['confirm_password'] == "":
        return jsonify(status="error", message="Please enter valid value")
    elif not new_user['password'] == new_user['confirm_password']:
        return jsonify(status="warning", message="Passwords didn't match")

    try:
        controllers.add_user(new_user['username'], new_user['password'], new_user['usertype'])
        activity.logger.error("New user added({}).".format(session['username']))
        return jsonify(status="success", message="User added")
    except Exception as e:
        print(e)
        activity.logger.error("Username is not available. Please select different username")
        return jsonify(status="warning", message="Username is not available. Please select different username")

@users.route('/<username>/password/', methods=['PUT'])
@is_user_logged_in("Illegal request for change {username}'s password event.")
def change_password(username):
    if not session['username'] == username:
        activity.logger.error("{} user request to change {} 's password. Change password event fail.".format(session['username'], username))
        return jsonify(status="error", message="You can only change own password.")

    data = request.get_json()
    old_password = data.get('oldpassword')
    new_password = data.get('newpassword')
    confirm_password = data.get('confirmpassword')
    if old_password == "" or new_password == "" or confirm_password == "":
        return jsonify(status="error", message="Please enter valid value")
    elif not new_password == confirm_password:
        activity.logger.error("Passwords didn't match for {} 's change password event. Change password event fail.".format(session['username']))
        return jsonify(status="error", message="Passwords didn't match")

    # Maybe there isn't any user for the username
    result = controllers.validate_user(username, old_password)
    if not result:
        activity.logger.error("Old password is wrong for {} 's change password event. Change password event fail.".format(session['username']))
        return jsonify(status="error", message="Old password is wrong")

    controllers.update_user_password(username, new_password)
    activity.logger.error("{} user change own password.".format(session['username']))
    return jsonify(status="success")