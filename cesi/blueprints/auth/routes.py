from flask import (
    Blueprint,
    jsonify,
    session,
    request,
    g
)

from core import Cesi
from decorators import (
    is_user_logged_in,
    is_admin
)
from loggers import ActivityLog

auth = Blueprint('auth', __name__)
cesi = Cesi.getInstance()
activity = ActivityLog.getInstance()

@auth.route('/login/', methods = ['POST'])
def login():
    data = request.get_json()
    req_username, req_password = data.get('username'), data.get('password')
    cur = g.db_conn.cursor()
    cur.execute("select * from userinfo where username=? and password=?",(req_username, req_password))
    result = cur.fetchall()
    if not result:
        session.clear()
        return jsonify(status="error", message="Invalid username/password")

    username, _, usertype = result[0]
    session['username'] = username
    session['logged_in'] = True
    session['usertypecode'] = usertype
    activity.logger.info("{} logged in.".format(session['username']))
    return jsonify(status="success", message="Valid username/password")

@auth.route('/logout/', methods = ['POST'])
def logout():
    activity.logger.error("{} logged out".format(session['username']))
    session.clear()
    return jsonify(status="success", message="Logout")
