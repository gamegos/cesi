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
    session
)

from core import (
    Cesi
)
from decorators import (
    is_user_logged_in,
    is_admin,
    is_admin_or_normal_user
)
from util import (
    ActivityLog,
    JsonValue
)

VERSION = "v2"

app = Flask(__name__)
app.config.from_object(__name__)

cesi = None
activity = None

# Database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = cesi.get_db_connection()
    return db

# Close database connection
@app.teardown_appcontext
def close_connection(_):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route(f'/{VERSION}/userinfo')
@is_user_logged_in()
def user_info():
    return jsonify(username=session['username'], usertypecode=session['usertype'])

# Render login page or username, password control
@app.route('/login', methods = ['GET', 'POST'])
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
                session['usertype'] = cur.fetchall()[0][2]
                activity.logger.info("{} logged in.".format(session['username']))
                return redirect('/')
            else:
                session.clear()
                activity.logger.info("Login fail. Invalid password.")
                return redirect('/login?code=invalid')

    code = request.args.get('code', '')
    return render_template('login.html', code = code, name = cesi.name)

# Logout action
@app.route(f'/{VERSION}/logout', methods = ['GET', 'POST'])
def logout():
    activity.logger.error("{} logged out".format(session['username']))
    session.clear()
    return redirect('/login')

@app.route(f'/{VERSION}/users')
@is_user_logged_in()
@is_admin("Unauthorized user request for delete user event. Delete user event fail.")
def user_list():
    cur = get_db().cursor()
    cur.execute("select username, type from userinfo")
    result = cur.fetchall()
    users = [ {'name': str(element[0]), 'type': str(element[1])} for element in result]
    return jsonify(status = 'success',
                    users = users)

@app.route(f'/{VERSION}/delete/user/<username>')
@is_user_logged_in("Illegal request for delete {username} user event.")
@is_admin("{user} is unauthorized user for request to delete {username} user. Delete event fail.")
def del_user_handler(username):
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
@app.route(f'/{VERSION}/add/user/handler', methods = ['GET', 'POST'])
@is_user_logged_in("Illegal request for add user event.")
@is_admin("{user} is unauthorized user for request to add user event. Add user event fail.")
def adduserhandler():
    username = request.form['username']
    password = request.form['password']
    confirmpassword = request.form['confirmpassword']

    if username == "" or password == "" or confirmpassword == "":
        return jsonify( status = "null",
                        message = "Please enter value")
    else:
        if request.form['usertype'] == "Admin":
            usertype = 0
        elif request.form['usertype'] == "Standart User":
            usertype = 1
        elif request.form['usertype'] == "Only Log":
            usertype = 2
        elif request.form['usertype'] == "Read Only":
            usertype = 3

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

@app.route(f'/{VERSION}/change/password/<username>/handler', methods=['POST'])
@is_user_logged_in("Illegal request for change {username}'s password event.")
def changepasswordhandler(username):
    if session['username'] == username:
        cur = get_db().cursor()
        cur.execute("select password from userinfo where username=?",(username,))
        ar=[str(r[0]) for r in cur.fetchall()]
        if request.form['old'] == ar[0]:
            if request.form['new'] == request.form['confirm']:
                if request.form['new'] != "":
                    cur.execute("update userinfo set password=? where username=?",[request.form['new'], username])
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

@app.route(f'/{VERSION}/activitylog')
@is_user_logged_in()
def get_activity_log():
    with open(cesi.activity_log) as f:
        data = f.readlines()
        return jsonify(status="success",
                        log=data)

@app.route(f'/{VERSION}/activitylog/<int:limit>')
@is_user_logged_in()
def get_activity_log_with_limit(limit):
    with open(cesi.activity_log) as f:
        data = f.readlines()
        return jsonify(status="success",
                        log=data[-limit:])

#### Cesi Routes
@app.route(f'/{VERSION}/environments')
@is_user_logged_in()
def get_environments():
    return jsonify(cesi.serialize_environments())

@app.route(f'/{VERSION}/environments/<env_name>')
@is_user_logged_in()
def get_environment_details(env_name):
    _environment = cesi.get_environment_or_400(env_name)
    return jsonify(_environment.serialize())

@app.route(f'/{VERSION}/groups')
@is_user_logged_in()
@is_admin()
def get_groups():
    _groups = set()
    for node in cesi.nodes:
        if node.is_connected:
            for p in node.processes:
                _groups.add(p.group)
        else:
            print(f"{node.name} is not connected.")

    # Set is not JSON serializable.
    return jsonify(groups=list(_groups))

@app.route(f'/{VERSION}/groups/<group_name>')
@is_user_logged_in()
@is_admin()
def get_group_details(group_name):
    return jsonify({})
    #return jsonify(get_group_details(cesi, group_name))

@app.route(f'/{VERSION}/nodes')
@is_user_logged_in()
def get_node_names():
    connected = []
    not_connected = []
    for node in cesi.nodes:
        if node.is_connected:
            connected.append(node.name)
        else:
            not_connected.append(node.name)

    return jsonify(
        nodes={
            'connected': connected,
            'not_connected': not_connected
        }
    )

@app.route(f'/{VERSION}/nodes/<node_name>')
@is_user_logged_in()
def get_node(node_name):
    node = cesi.get_node_or_400(node_name)
    return jsonify(node.serialize())

@app.route(f'/{VERSION}/nodes/<node_name>/processes')
@is_user_logged_in()
def get_node_processes(node_name):
    node = cesi.get_node_or_400(node_name)
    if node.is_connected:
        return jsonify(node.serialize_processes())
    else:
        return jsonify(message="Node is not connected")

@app.route(f'/{VERSION}/nodes/<node_name>/processes/<process_name>')
@is_user_logged_in()
def get_process(node_name, process_name):
    node = cesi.get_node_or_400(node_name)
    if node.is_connected:
        process = node.get_process_or_400(process_name)
        return jsonify(process.serialize())
    else:
        return jsonify(message="Node is not connected")

@app.route(f'/{VERSION}/nodes/<node_name>/processes/<process_name>/start')
@is_user_logged_in("Illegal request for start to {node_name} node's {process_name} process.")
@is_admin_or_normal_user("{user} is unauthorized user request for start.Start event fail for {node_name} node's {process_name} process.")
def start_process(node_name, process_name):
    node = cesi.get_node_or_400(node_name)
    if node.is_connected:
        status, msg = node.start_process(process_name)
        if status:
            activity.logger.info("{} started {} node's {} process.".format(session['username'], node_name, process_name))
            return JsonValue.success(node=node, process_name=process_name, event_name="start")
        else:
            activity.logger.info("{} unsuccessful start event {} node's {} process.".format(session['username'], node_name, process_name))
            return jsonify(message=msg)
    else:
        return jsonify(message="Node is not connected")

@app.route(f'/{VERSION}/nodes/<node_name>/processes/<process_name>/stop')
@is_user_logged_in("Illegal request for stop to {node_name} node's {process_name} process.")
@is_admin_or_normal_user("{user} is unauthorized user request for stop.Stop event fail for {node_name} node's {process_name} process.")
def stop_process(node_name, process_name):
    node = cesi.get_node_or_400(node_name)
    if node.is_connected:
        status, msg = node.stop_process(process_name)
        if status:
            activity.logger.info("{} stopped {} node's {} process.".format(session['username'], node_name, process_name))
            return JsonValue.success(node=node, process_name=process_name, event_name="stop")
        else:
            activity.logger.info("{} unsuccessful stop event {} node's {} process.".format(session['username'], node_name, process_name))
            return jsonify(message=msg)
    else:
        return jsonify(message="Node is not connected")

@app.route(f'/{VERSION}/nodes/<node_name>/processes/<process_name>/restart')
@is_user_logged_in("Illegal request for restart to {node_name} node's {process_name} process.")
@is_admin_or_normal_user("{user} is unauthorized user request for restart.Restart event fail for {node_name} node's {process_name} process.")
def restart_process(node_name, process_name):
    node = cesi.get_node_or_400(node_name)
    if node.is_connected:
        status, msg = node.restart_process(process_name)
        if status:
            activity.logger.info("{} restarted {} node's {} process.".format(session['username'], node_name, process_name))
            return JsonValue.success(node=node, process_name=process_name, event_name="restart")
        else:
            activity.logger.info("{} unsuccessful restart event {} node's {} process.".format(session['username'], node_name, process_name))
            return jsonify(message=msg)
    else:
        return jsonify(message="Node is not connected")

@app.route(f'/{VERSION}/nodes/<node_name>/processes/<process_name>/log')
@is_user_logged_in("Illegal request for read log to {node_name} node's {process_name} process.")
def read_process_log(node_name, process_name):
    if session['usertype'] == 0 or session['usertype'] == 1 or session['usertype'] == 2:
        node = cesi.get_node_or_400(node_name)
        if node.is_connected:
            log_string = node.connection.supervisor.tailProcessStdoutLog(process_name, 0, 500)[0]
            log_list = log_string.split("\n")[1:-1]
            activity.logger.info("{} read log {} node's {} process.".format(session['username'], node_name, process_name))
            return jsonify(status="success", log=log_list)
        else:
            return jsonify(message="Node is not connected")
    else:
        activity.logger.info("{} is unauthorized user request for read log. Read log event fail for {} node's {} process.".format(session['username'], node_name, process_name))
        return jsonify(status="error", message="You are not authorized for this action")

@app.route(f'/{VERSION}/nodes/<node_name>/all-processes/start')
@is_user_logged_in("Illegal request for start to {node_name} node's all processes.")
@is_admin_or_normal_user("{user} unauthorized user request for start.Start event fail for {node_name} node's all processes.")
def start_all_process(node_name):
    node = cesi.get_node_or_400(node_name)
    if node.is_connected:
        for process in node.processes:
            if not process.state == 20:
                status, msg = node.start_process(process.name)
                if status:
                    activity.logger.info("{} started {} node's {} process.".format(session['username'], node_name, process.name))
                else:
                    activity.logger.info("{} unsuccessful start event {} node's {} process.".format(session['username'], node_name, process.name))

        return jsonify(message="success")
    else:
        return jsonify(message="Node is not connected")

@app.route(f'/{VERSION}/nodes/<node_name>/all-processes/stop')
@is_user_logged_in("Illegal request for stop to {node_name} node's all processes.")
@is_admin_or_normal_user("{user} unauthorized user request for stop.Stop event fail for {node_name} node's all processes.")
def stop_all_process(node_name):
    node = cesi.get_node_or_400(node_name)
    if node.is_connected:
        for process in node.processes:
            if not process.state == 0:
                status, msg = node.stop_process(process.name)
                if status:
                    activity.logger.info("{} stopped {} node's {} process.".format(session['username'], node_name, process.name))
                else:
                    activity.logger.info("{} unsuccessful stop event {} node's {} process.".format(session['username'], node_name, process.name))

        return jsonify(message="success")
    else:
        return jsonify(message="Node is not connected")

@app.route(f'/{VERSION}/nodes/<node_name>/all-processes/restart')
@is_user_logged_in("Illegal request for restart to {node_name} node's all processes.")
@is_admin_or_normal_user("{user} unauthorized user request for restart.Restart event fail for {node_name} node's all processes.")
def restart_all_process(node_name):
    node = cesi.get_node_or_400(node_name)
    if node.is_connected:
        for process in node.processes:
            if not process.state == 0:
                status, msg = node.stop_process(process.name)
                if status:
                    print("Process stopped!")
                else:
                    print(msg)

            status, msg = node.start_process(process.name)
            if status:
                activity.logger.info("{} restarted {} node's {} process.".format(session['username'], node_name, process.name))
            else:
                activity.logger.info("{} unsuccessful restart event {} node's {} process.".format(session['username'], node_name, process.name))

        return jsonify(message="success")
    else:
        return jsonify(message="Node is not connected")

@app.route(f'/{VERSION}/initdb')
def initdb():
    cesi.drop_database()
    cesi.check_database()
    return jsonify(message="Success")

@app.route('/')
def showMain():
    # get user type
    if session.get('logged_in'):
        if session['usertype']==0:
            usertype = "Admin"
        elif session['usertype']==1:
            usertype = "Standart User"
        elif session['usertype']==2:
            usertype = "Only Log"
        elif session['usertype']==3:
            usertype = "Read Only"

        return render_template('index.html',
                                name = cesi.name,
                                theme = cesi.theme,
                                username = session['username'],
                                usertype = usertype,
                                usertypecode = session['usertype'])
    else:
         return redirect('/login')

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

    app.run(
        host=cesi.host,
        port=cesi.port,
        use_reloader=cesi.auto_reload,
        debug=cesi.debug,
    )