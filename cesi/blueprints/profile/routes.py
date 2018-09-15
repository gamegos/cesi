from flask import (
    Blueprint,
    jsonify,
    session,
    request
)

from decorators import is_user_logged_in
from loggers import ActivityLog
import controllers

profile = Blueprint('profile', __name__)
activity = ActivityLog.getInstance()

@profile.route('/', methods=['GET'])
@is_user_logged_in("Illegal request to get your own information")
def get_own_info():
    user = controllers.get_user(session['username'])
    print(user)
    return jsonify(status='success', user=user)

@profile.route('/password/', methods=['PUT'])
@is_user_logged_in("Illegal request to change your own password.")
def change_own_password():
    data = request.get_json()
    old_password = data.get('oldpassword')
    new_password = data.get('newpassword')
    confirm_password = data.get('confirmpassword')
    if old_password == "" or new_password == "" or confirm_password == "":
        return jsonify(status="error", message="Please enter valid value")
    elif not new_password == confirm_password:
        activity.logger.error("Passwords didn't match to change {} 's password.".format(session['username']))
        return jsonify(status="error", message="Passwords didn't match")

    # Maybe there isn't any user for the username
    result = controllers.validate_user(username, old_password)
    if not result:
        activity.logger.error("Old password is wrong to change {} 's password.".format(session['username']))
        return jsonify(status="error", message="Old password is wrong")

    controllers.update_user_password(username, new_password)
    activity.logger.error("{} user changed the own password.".format(session['username']))
    return jsonify(status="success")