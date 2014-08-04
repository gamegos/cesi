from flask import Flask, render_template, url_for, redirect, jsonify, request
from getProcInfo import Config, Connection, Node, CONFIG_FILE, ProcessInfo, JsonValue
import getProcInfo 
import xmlrpclib
import sqlite3

DATABASE = "./userinfo.db"

app = Flask(__name__)
app.config.from_object(__name__)
session=0

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/login/control', methods = ['GET', 'POST'])
def control():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        cur = get_db().cursor()
        cur.execute("select * from userinfo where username=?",(username,))
        if not cur.fetchall():
            return "Username is not available"
        else:
            cur.execute("select * from userinfo where username=?",(username,))
            if password == cur.fetchall()[0][1]:
                global session
                session = 1
                return redirect(url_for('showMain'))
            else:
                return "Invalid password"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    global session
    session = 0
    return redirect(url_for('login'))

@app.route('/')
def showMain():
    if session ==1:
        all_process_count = 0
        running_process_count = 0
        stopped_process_count = 0
        node_count = 0
        node_name_list = []
        for nodename in Config(CONFIG_FILE).getAllNodeNames():
            node_count = node_count + 1
            nodename = nodename[5:]
            node_name_list.append(nodename)
            nodeconfig = Config(CONFIG_FILE).getNodeConfig(nodename)
            node = Node(nodeconfig)
            for process in node.process_list:
                all_process_count = all_process_count + 1
                if process.state==20:
                    running_process_count = running_process_count + 1
                if process.state==0:
                    stopped_process_count = stopped_process_count + 1

        return render_template('index.html', all_process_count =all_process_count, running_process_count =running_process_count, stopped_process_count =stopped_process_count, node_count =node_count, node_name_list = node_name_list)
    else:
        return redirect(url_for('login'))
@app.route('/node/<node_name>')
def showNode(node_name):
    node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
    return jsonify( process_info = Node(node_config).process_dict )

@app.route('/node/<node_name>/process/<process_name>/restart')
def json_restart(node_name, process_name):
    try:
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        if node.connection.supervisor.stopProcess(process_name):
            if node.connection.supervisor.startProcess(process_name):
                return JsonValue(process_name, node_name, "restart").success()
    except xmlrpclib.Fault as err:
        return JsonValue(process_name, node_name, "restart").error(err.faultCode, err.faultString)

@app.route('/node/<node_name>/process/<process_name>/start')
def json_start(node_name, process_name):
    try:
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        if node.connection.supervisor.startProcess(process_name):
            return JsonValue(process_name, node_name, "start").success()
    except xmlrpclib.Fault as err:
        return JsonValue(process_name, node_name, "start").error(err.faultCode, err.faultString)

@app.route('/node/<node_name>/process/<process_name>/stop')
def json_stop(node_name, process_name):
    try:
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        if node.connection.supervisor.stopProcess(process_name):
            return JsonValue(process_name, node_name, "stop").success()
    except xmlrpclib.Fault as err:
        return JsonValue(process_name, node_name, "stop").error(err.faultCode, err.faultString)

@app.route('/node/name/list')
def getlist():
    node_name_list = []
    node_names = Config(CONFIG_FILE).getAllNodeNames()
    for node_name in node_names:
        node_name_list.append(node_name[5:])
    return jsonify( node_name_list = node_name_list )


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

try:
    if __name__ == '__main__':
        app.run(debug=True, use_reloader=True)
except xmlrpclib.Fault as err:
    print "A fault occurred"
    print "Fault code: %d" % err.faultCode
    print "Fault string: %s" % err.faultString
