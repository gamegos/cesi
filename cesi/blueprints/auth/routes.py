from flask import (
    Blueprint,
    jsonify,
    session,
    redirect,
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
    username = request.form['username']
    password = request.form['password']
    cur = g.db_conn.cursor()
    cur.execute("select * from userinfo where username=?",(username,))
    #if query returns an empty list
    if not cur.fetchall():
        session.clear()
        activity.logger.info("Login fail. Username is not available.")
        return redirect('/login?code=invalid')
    else:
        cur.execute("select * from userinfo where username=?",(username,))

        if password == cur.fetchall()[0][1]:
            session['username'] = username
            session['logged_in'] = True
            cur.execute("select * from userinfo where username=?",(username,))
            session['usertypecode'] = cur.fetchall()[0][2]
            activity.logger.info("{} logged in.".format(session['username']))
            return redirect('/')
        else:
            session.clear()
            activity.logger.info("Login fail. Invalid password.")
            return redirect('/login?code=invalid')

@auth.route('/logout/', methods = ['POST'])
def logout():
    activity.logger.error("{} logged out".format(session['username']))
    session.clear()
    return redirect(url_for('login'))
