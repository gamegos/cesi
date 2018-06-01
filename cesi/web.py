from flask import Flask, render_template, redirect, jsonify, request, g, session
from cesi import Config, Node, CONFIG_FILE, JsonValue, cesi, NodeConfig, get_groups, get_group_details
from datetime import datetime
import xmlrpclib
import sqlite3
import mmap
import os


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '42'

DATABASE = Config(CONFIG_FILE).getDatabase()
ACTIVITY_LOG = Config(CONFIG_FILE).getActivityLog()
HOST = Config(CONFIG_FILE).getHost()
VERSION = "v2"


# Database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# Close database connection
@app.teardown_appcontext
def close_connection(_):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/{}/environments'.format(VERSION))
def get_env_names():
    if session.get('logged_in'):
        env_list = []
        for k in cesi['environments']:
            env_list.append(k)
        return jsonify(environments=env_list)

    else:
        return jsonify(message='Session expired'), 403


@app.route('/{}/environments/<env_name>'.format(VERSION))
def get_env_nodes(env_name):
    if session.get('logged_in'):
        try:
            return jsonify(nodes=cesi['environments'][env_name])

        except Exception as _:
            return jsonify(message="Wrong environment name")

    else:
        return jsonify(message='Session expired'), 403


@app.route('/{}/nodes'.format(VERSION))
def get_node_names():
    if session.get('logged_in'):
        connected = []
        not_connected = []
        for nodename in cesi['nodes']:
            n = cesi['nodes'][nodename]
            try:
                node = Node(NodeConfig("node:" + n['name'], n['host'], n['port'], n['username'], n['password']))
                if node.is_connected and nodename not in connected:
                    connected.append(nodename)
                elif nodename not in not_connected:
                    not_connected.append(nodename)

            except Exception as _:
                 if nodename not in not_connected:
                     not_connected.append(nodename)

        return jsonify(nodes={'connected': connected, 'not_connected': not_connected})

    else:
        return jsonify(message='Session expired'), 403


@app.route('/{}/nodes/<node_name>'.format(VERSION))
def get_node(node_name):
    if session.get('logged_in'):
        try:
            n = cesi['nodes'][node_name]
            try:
                _ = Node(NodeConfig("node:" + n['name'], n['host'], n['port'], n['username'], n['password']))
                return jsonify({
                                'name': n['name'],
                                'host': n['host'],
                                'port': n['port'],
                                'connected': True
                            })

            except Exception as _:
                return jsonify({
                                'name': n['name'],
                                'host': n['host'],
                                'port': n['port'],
                                'connected': False
                            })

        except Exception as _:
            return jsonify(message="Wrong node name")

    else:
        return jsonify(message='Session expired'), 403


@app.route('/{}/nodes/<node_name>/processes'.format(VERSION))
def get_node_processes(node_name):
    if session.get('logged_in'):
        try:
            n = cesi['nodes'][node_name]

        except Exception as _:
            return jsonify(message="Wrong node name")

        try:
            node = Node(NodeConfig("node:" + n['name'], n['host'], n['port'], n['username'], n['password']))
            return jsonify(processes=node.get_processes())

        except Exception as _:
            return jsonify(message="Node is not connected")

    else:
        return jsonify(message='Session expired'), 403


@app.route('/{}/nodes/<node_name>/processes/<pro_name>'.format(VERSION))
def get_process(node_name, pro_name):
    if session.get('logged_in'):
        try:
            n = cesi['nodes'][node_name]

        except Exception as _:
            return jsonify(message="Wrong node name")

        try:
            node = Node(NodeConfig("node:" + n['name'], n['host'], n['port'], n['username'], n['password']))
            try:
                return jsonify(node.get_processes()[pro_name])

            except Exception as _:
                return jsonify(message="Wrong process name")

        except Exception as _:
            return jsonify(message="Node is not connected")

    else:
        return jsonify(message='Session expired'), 403


@app.route('/{}/nodes/<node_name>/processes/<process_name>/start'.format(VERSION))
def start_process(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1:
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                group = node.get_processes()[process_name]["group"]
                process_name = group + ":" + process_name
                if node.connection.supervisor.startProcess(process_name):
                    add_log = open(ACTIVITY_LOG, "a")
                    add_log.write("%s - %s started %s node's %s process .\n" % (datetime.now().ctime(),
                                                                                session['username'],
                                                                                node_name,
                                                                                process_name))
                    return JsonValue(process_name, node_name, "start").success()
                else:
                    return jsonify(status="error1",
                                   message="Cannot start process")
            except xmlrpclib.Fault as er:
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s unsuccessful start event %s node's %s process .\n"
                              % (datetime.now().ctime(), session['username'], node_name, process_name))
                return JsonValue(process_name, node_name, "start").error(er.faultCode, er.faultString)
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for start. "
                          "Start event fail for %s node's %s process .\n"
                          % (datetime.now().ctime(), session['username'], node_name, process_name))
            return jsonify(status="error2",
                           message="You are not authorized this action")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for start to %s node's %s process .\n" % (datetime.now().ctime(),
                                                                                      node_name,
                                                                                      process_name))
        return jsonify(message='Session expired'), 403


@app.route('/{}/nodes/<node_name>/processes/<process_name>/stop'.format(VERSION))
def stop_process(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1:
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                group = node.get_processes()[process_name]["group"]
                process_name = group + ":" + process_name
                if node.connection.supervisor.stopProcess(process_name):
                    add_log = open(ACTIVITY_LOG, "a")
                    add_log.write("%s - %s stopped %s node's %s process .\n" % (datetime.now().ctime(),
                                                                                session['username'],
                                                                                node_name,
                                                                                process_name))
                    return JsonValue(process_name, node_name, "stop").success()
                else:
                    return jsonify(status="error1",
                                   message="Cannot stop process")
            except xmlrpclib.Fault as er:
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s unsuccessful stop event %s node's %s process .\n"
                              % (datetime.now().ctime(), session['username'], node_name, process_name))
                return JsonValue(process_name, node_name, "stop").error(er.faultCode, er.faultString)
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for start. "
                          "Stop event fail for %s node's %s process .\n"
                          % (datetime.now().ctime(), session['username'], node_name, process_name))
            return jsonify(status="error2",
                           message="You are not authorized this action")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for stop to %s node's %s process .\n" % (datetime.now().ctime(),
                                                                                     node_name,
                                                                                     process_name))
        return jsonify(message='Session expired'), 403


@app.route('/{}/nodes/<node_name>/processes/<process_name>/restart'.format(VERSION))
def restart_process(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1:
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                pro = node.get_processes()[process_name]
                group = pro["group"]
                process_name = group + ":" + process_name
                if pro["state"] == 20:
                    node.connection.supervisor.stopProcess(process_name)

                if node.connection.supervisor.startProcess(process_name):
                    add_log = open(ACTIVITY_LOG, "a")
                    add_log.write("%s - %s restarted %s node's %s process .\n" % (datetime.now().ctime(),
                                                                                  session['username'],
                                                                                  node_name,
                                                                                  process_name))
                    return JsonValue(process_name, node_name, "restart").success()
                else:
                    return jsonify(status="error1",
                                   message="Cannot restart process")
            except xmlrpclib.Fault as er:
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s unsuccessful restart event %s node's %s process .\n"
                              % (datetime.now().ctime(), session['username'], node_name, process_name))
                return JsonValue(process_name, node_name, "restart").error(er.faultCode, er.faultString)
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for start. "
                          "Restart event fail for %s node's %s process .\n"
                          % (datetime.now().ctime(), session['username'], node_name, process_name))
            return jsonify(status="error2",
                           message="You are not authorized this action")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for restart to %s node's %s process .\n" % (datetime.now().ctime(),
                                                                                        node_name,
                                                                                        process_name))
        return jsonify(message='Session expired'), 403


@app.route('/{}/nodes/<node_name>/processes/<process_name>/log'.format(VERSION))
def process_read_log(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1 or session['usertype'] == 2:
            node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
            node = Node(node_config)
            group = node.get_processes()[process_name]["group"]
            process_name = group + ":" + process_name
            log = node.connection.supervisor.tailProcessStdoutLog(process_name, 0, 500)[0].split("\n")[1:-1]
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s read log %s node's %s process .\n" % (datetime.now().ctime(),
                                                                         session['username'],
                                                                         node_name, process_name))
            return jsonify(status="success", log=log)
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write(
                "%s - %s is unauthorized user request for read log. Read log event fail for %s node's %s process .\n"
                %
                (datetime.now().ctime(), session['username'], node_name, process_name))
            return jsonify(status="error", message="You are not authorized for this action")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for read log to %s node's %s process .\n" % (datetime.now().ctime(),
                                                                                         node_name,
                                                                                         process_name))
        return jsonify(status="error", message="First login please")


@app.route('/{}/nodes/<node_name>/all-processes'.format(VERSION))
def get_node_all_processes(node_name):
    if session.get('logged_in'):
        try:
            n = cesi['nodes'][node_name]

        except Exception as _:
            return jsonify(message="Wrong node name")

        try:
            node = Node(NodeConfig("node:" + n['name'], n['host'], n['port'], n['username'], n['password']))
            return jsonify(processes=node.get_processes())

        except Exception as _:
            return jsonify(message="Node is not connected")

    else:
        return jsonify(message='Session expired'), 403


@app.route('/{}/nodes/<node_name>/all-processes/start'.format(VERSION))
def start_all_process(node_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1:
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                pros = node.get_processes()
                for process_name in pros:
                    group = pros[process_name]["group"]
                    if pros[process_name]["state"] == 20:
                        continue
                    process_name = group + ":" + process_name
                    try:
                        if node.connection.supervisor.startProcess(process_name):
                            add_log = open(ACTIVITY_LOG, "a")
                            add_log.write("%s - %s started %s node's %s process .\n" % (datetime.now().ctime(),
                                                                                        session['username'],
                                                                                        node_name,
                                                                                        process_name))
                    except xmlrpclib.Fault as _:
                        add_log = open(ACTIVITY_LOG, "a")
                        add_log.write("%s - %s unsuccessful start event %s node's %s process .\n"
                                      % (datetime.now().ctime(), session['username'], node_name, process_name))
                        continue

                return jsonify(message="success")

            except Exception as _:
                return jsonify(message="Wrong node name")

        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for start. "
                          "Start event fail for %s node's all processes .\n"
                          % (datetime.now().ctime(), session['username'], node_name))
            return jsonify(status="error2",
                           message="You are not authorized this action")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for start to %s node's all processes .\n" % (datetime.now().ctime(),
                                                                                         node_name))
        return jsonify(message='Session expired'), 403


@app.route('/{}/nodes/<node_name>/all-processes/stop'.format(VERSION))
def stop_all_process(node_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1:
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                pros = node.get_processes()
                for process_name in pros:
                    group = pros[process_name]["group"]
                    if pros[process_name]["state"] == 0:
                        continue
                    process_name = group + ":" + process_name
                    try:
                        if node.connection.supervisor.stopProcess(process_name):
                            add_log = open(ACTIVITY_LOG, "a")
                            add_log.write("%s - %s stopped %s node's %s process .\n" % (datetime.now().ctime(),
                                                                                        session['username'],
                                                                                        node_name,
                                                                                        process_name))
                    except xmlrpclib.Fault as _:
                        add_log = open(ACTIVITY_LOG, "a")
                        add_log.write("%s - %s unsuccessful stop event %s node's %s process .\n"
                                      % (datetime.now().ctime(), session['username'], node_name, process_name))
                        continue

                return jsonify(message="success")

            except Exception as _:
                return jsonify(message="Wrong node name")

        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for stop. "
                          "Stop event fail for %s node's all processes .\n"
                          % (datetime.now().ctime(), session['username'], node_name))
            return jsonify(status="error2",
                           message="You are not authorized this action")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for stop to %s node's all processes .\n" % (datetime.now().ctime(),
                                                                                        node_name))
        return jsonify(message='Session expired'), 403


@app.route('/{}/nodes/<node_name>/all-processes/restart'.format(VERSION))
def restart_all_process(node_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1:
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                pros = node.get_processes()
                for process_name in pros:
                    group = pros[process_name]["group"]
                    process_name = group + ":" + process_name
                    try:
                        if node.connection.supervisor.stopProcess(process_name):
                            node.connection.supervisor.startProcess(process_name)
                            add_log = open(ACTIVITY_LOG, "a")
                            add_log.write("%s - %s restarted %s node's %s process .\n" % (datetime.now().ctime(),
                                                                                          session['username'],
                                                                                          node_name,
                                                                                          process_name))
                    except xmlrpclib.Fault as _:
                        add_log = open(ACTIVITY_LOG, "a")
                        add_log.write("%s - %s unsuccessful restart event %s node's %s process .\n"
                                      % (datetime.now().ctime(), session['username'], node_name, process_name))
                        continue

                return jsonify(message="success")

            except Exception as _:
                return jsonify(message="Wrong node name")

        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for restart. "
                          "Restart event fail for %s node's all processes .\n"
                          % (datetime.now().ctime(), session['username'], node_name))
            return jsonify(status="error2",
                           message="You are not authorized this action")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for restart to %s node's all processes .\n" % (datetime.now().ctime(),
                                                                                           node_name))
        return jsonify(message='Session expired'), 403


@app.route('/{}/groups'.format(VERSION))
def get_group_names():
    if session.get('logged_in'):
        return jsonify(groups=get_groups(cesi))

    else:
        return jsonify(message='Session expired'), 403


@app.route('/{}/groups/<group_name>'.format(VERSION))
def get_group_information(group_name):
    if session.get('logged_in'):
        return jsonify(get_group_details(cesi, group_name))

    else:
        return jsonify(message='Session expired'), 403


@app.route('/{}/activitylog'.format(VERSION))
def get_log_tail():
    fm = file
    n = 12
    try:
        lines = []
        size = os.path.getsize(ACTIVITY_LOG)
        with open(ACTIVITY_LOG, "rb") as f:
            # for Windows the mmap parameters are different
            fm = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
        for i in xrange(size - 1, -1, -1):
            if fm[i] == '\n':
                n -= 1
                if n == -1:
                    break
            lines = fm[i + 1 if i else 0:].splitlines()
        return jsonify(status="success",
                       log=lines)
    except Exception as er:
        return jsonify(status="error",
                       messagge=er)
    finally:
        try:
            fm.close()
        except (UnboundLocalError, TypeError):
            return jsonify(status="error",
                           message="Activity log file is empty")


@app.route('/{}/userinfo'.format(VERSION))
def user_info():
   if session.get('logged_in'):
       return jsonify(username=session['username'], usertypecode=session['usertype'])
   else:
      return jsonify(message='Session expired'), 403


# Username and password control
@app.route('/login/control', methods = ['POST'])
def control():
    username = request.form['username']
    password = request.form['password']
    cur = get_db().cursor()
    cur.execute("select * from userinfo where username=?",(username,))
#if query returns an empty list
    if not cur.fetchall():
        session.clear()
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Login fail. Username is not available.\n"%( datetime.now().ctime() ))
        return redirect('/login?code=invalid')
    else:
        cur.execute("select * from userinfo where username=?",(username,))
        
        if password == cur.fetchall()[0][1]:
            session['username'] = username
            session['logged_in'] = True
            cur.execute("select * from userinfo where username=?",(username,))
            session['usertype'] = cur.fetchall()[0][2]
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s logged in.\n"%( datetime.now().ctime(), session['username'] ))
            return redirect('/')
        else:
            session.clear()
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - Login fail. Invalid password.\n"%( datetime.now().ctime() ))
            return redirect('/login?code=invalid')

# Render login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    code = request.args.get('code', '')
    return render_template('login.html', code = code, name = Config(CONFIG_FILE).getName())

# Logout action
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    add_log = open(ACTIVITY_LOG, "a")
    add_log.write("%s - %s logged out.\n"%( datetime.now().ctime(), session['username'] ))
    session.clear()
    return redirect('/login')

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
                                name = Config(CONFIG_FILE).getName(),
                                theme = Config(CONFIG_FILE).getTheme(),
                                username = session['username'],
                                usertype = usertype,
                                usertypecode = session['usertype'])
    else:
         return redirect('/login')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

try:
    if __name__ == '__main__':
        app.run(debug=True, 
         host='0.0.0.0', 
         port=Config(CONFIG_FILE).getPort(),
         threaded=True)
except xmlrpclib.Fault as err:
    print "A fault occurred"
    print "Fault code: %d" % err.faultCode
    print "Fault string: %s" % err.faultString
