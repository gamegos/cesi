import os
import sys
import argparse
import xmlrpc.client

from flask import (
    Flask,
    render_template,
    redirect,
    jsonify,
    request,
    g,
    session,
    url_for
)

from core import Cesi
from decorators import (
    is_user_logged_in,
    is_admin,
    is_admin_or_normal_user
)
from loggers import ActivityLog
from util import (
    JsonValue,
    get_db
)

VERSION = "v2"

app = Flask(__name__)
app.config.from_object(__name__)

cesi = None
activity = None

# Close database connection
@app.teardown_appcontext
def close_connection(_):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route(f'/{VERSION}/userinfo')
@is_user_logged_in()
def user_info():
    return jsonify(username=session['username'], usertypecode=session['usertypecode'])

# Render login page or username, password control
@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = get_db().cursor()
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

    code = request.args.get('code', '')
    return render_template('login.html', code = code, name = cesi.name)

# Logout action
@app.route(f'/{VERSION}/logout/', methods = ['GET', 'POST'])
def logout():
    activity.logger.error("{} logged out".format(session['username']))
    session.clear()
    return redirect(url_for('login'))

@app.route(f'/{VERSION}/initdb/')
def initdb():
    cesi.drop_database()
    cesi.check_database()
    return jsonify(message="Success")

@app.route('/')
def showMain():
    # get user type
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    username = session['username']
    usertypecode = session['usertypecode']
    return render_template('index.html',
                            name = cesi.name,
                            theme = cesi.theme,
                            username = username,
                            usertypecode = usertypecode)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.errorhandler(400)
def not_found(error):
    return jsonify(message=error.description)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cesi web server')

    parser.add_argument('-c', '--config',
                        default="./cesi.default.conf",
                        type=str,
                        help='config file')

    args = parser.parse_args()
    cesi = Cesi(config_file_path=args.config)
    activity = ActivityLog(log_path=cesi.activity_log)
    app.secret_key = cesi.secret_key
    
    # or dynamic import
    from blueprints.nodes.routes import nodes
    from blueprints.activitylogs.routes import activitylogs
    from blueprints.environments.routes import environments
    from blueprints.groups.routes import groups
    from blueprints.users.routes import users
    app.register_blueprint(nodes, url_prefix=f"/{VERSION}/nodes")
    app.register_blueprint(activitylogs, url_prefix=f"/{VERSION}/activitylogs")
    app.register_blueprint(environments, url_prefix=f"/{VERSION}/environments")
    app.register_blueprint(groups, url_prefix=f"/{VERSION}/groups")
    app.register_blueprint(users, url_prefix=f"/{VERSION}/users")
    
    app.run(
        host=cesi.host,
        port=cesi.port,
        use_reloader=cesi.auto_reload,
        debug=cesi.debug,
    )