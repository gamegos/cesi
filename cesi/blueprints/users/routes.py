from flask import (
    Blueprint,
    jsonify,
    session,
    request
)

from core import Cesi
from decorators import (
    is_user_logged_in,
    is_admin
)
from util import get_db
from loggers import ActivityLog

users = Blueprint('users', __name__)
cesi = Cesi.getInstance()
activity = ActivityLog.getInstance()

@users.route('/', methods=['GET'])
@is_user_logged_in("Illegal request for display users event.")
@is_admin("Unauthorized user request for display users event. Display users event fail.")
def user_list():
    cur = get_db().cursor()
    cur.execute("select username, type from userinfo")
    result = cur.fetchall()
    users = [ {'name': str(element[0]), 'type': str(element[1])} for element in result]
    return jsonify(status = 'success',
                    users = users)

@users.route('/<username>/delete/', methods=["DELETE"])
@is_user_logged_in("Illegal request for delete {username} user event.")
@is_admin("Unauthorized user for request to delete {username} user. Delete event fail.")
def delete_user(username):
    if username != "admin":
        cur = get_db().cursor()
        cur.execute("delete from userinfo where username=?",[username])
        get_db().commit()
        activity.logger.error("{} user deleted.".format(session['username']))
        return jsonify(status = "success")
    else:
        activity.logger.error("{} user request for delete admin user. Delete admin user event fail.".format(session['username']))
        return jsonify(status = "error",
                        message= "Admin can't delete")

# Writes new user information to database
@users.route('/add/', methods = ['POST'])
@is_user_logged_in("Illegal request for add user event.")
@is_admin("Unauthorized user for request to add user event. Add user event fail.")
def adduserhandler():
    username = request.form['username']
    password = request.form['password']
    confirmpassword = request.form['confirmpassword']
    try:
        usertype = int(request.form['usertype'])
    except ValueError as e:
        return jsonify(status="warning",
                        message=str(e))

    if username == "" or password == "" or confirmpassword == "":
        return jsonify( status = "null",
                        message = "Please enter value")
    else:
        cur = get_db().cursor()
        cur.execute("select * from userinfo where username=?",(username,))
        if not cur.fetchall():
            if password == confirmpassword:
                cur.execute("insert into userinfo values(?, ?, ?)", (username, password, usertype,))
                get_db().commit()
                activity.logger.error("New user added({}).".format(session['username']))
                return jsonify(status = "success",
                                message ="User added")
            else:
                # Is it necessary?
                activity.logger.error("Passwords didn't match at add user event.")
                return jsonify(status = "warning",
                                message ="Passwords didn't match")
        else:
            activity.logger.error("Username is not available. Please select different username")
            return jsonify(status = "warning",
                            message ="Username is not available. Please select different username")

@users.route('/<username>/password/', methods=['PUT'])
@is_user_logged_in("Illegal request for change {username}'s password event.")
def change_password(username):
    if session['username'] == username:
        old_password = request.form['old']
        new_password = request.form['new']
        confirm_password = request.form['confirm']
        cur = get_db().cursor()
        cur.execute("select password from userinfo where username=?",(username,))
        ar=[str(r[0]) for r in cur.fetchall()]
        if old_password == ar[0]:
            if new_password == confirm_password:
                if new_password != "":
                    cur.execute("update userinfo set password=? where username=?",[new_password, username])
                    get_db().commit()
                    activity.logger.error("{} user change own password.".format(session['username']))
                    return jsonify(status = "success")
                else:
                    return jsonify(status = "null",
                                    message = "Please enter valid value")
            else:
                activity.logger.error("Passwords didn't match for {} 's change password event. Change password event fail.".format(session['username']))
                return jsonify(status = "error", message = "Passwords didn't match")
        else:
            activity.logger.error("Old password is wrong for {} 's change password event. Change password event fail.".format(session['username']))
            return jsonify(status = "error", message = "Old password is wrong")
    else:
        activity.logger.error("{} user request to change {} 's password. Change password event fail.".format(session['username'], username))
        return jsonify(status = "error", message = "You can only change own password.")