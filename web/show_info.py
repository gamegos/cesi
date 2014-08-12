from flask import Flask, render_template, url_for, redirect, jsonify, request, g, session, flash
from getProcInfo import Config, Connection, Node, CONFIG_FILE, ProcessInfo, JsonValue
import getProcInfo 
import xmlrpclib
import sqlite3

DATABASE = "./userinfo.db"

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '42' # :)

# Database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Close database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Username and password control
@app.route('/login/control', methods = ['GET', 'POST'])
def control():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        cur = get_db().cursor()
        cur.execute("select * from userinfo where username=?",(username,))
#if query returns an empty list
        if not cur.fetchall():
            session['logged_in'] = False
            session['usertype'] = " "
            return "Username is not available"
        else:
            cur.execute("select * from userinfo where username=?",(username,))
            if password == cur.fetchall()[0][1]:
                session['username'] = username
                session['logged_in'] = True
                cur.execute("select * from userinfo where username=?",(username,))
                session['usertype'] = cur.fetchall()[0][2]
                return redirect(url_for('showMain'))
            else:
                session['logged_in'] = False
                return "Invalid password"

# Render login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')

# Logout action
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session['logged_in'] = False
    session['usertype']= " "
    session['username'] = "undefined"
    return redirect(url_for('login'))

# Dashboard
@app.route('/')
def showMain():
    if session.get('logged_in'):
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

        return render_template('index.html', all_process_count =all_process_count, running_process_count =running_process_count, stopped_process_count =stopped_process_count, node_count =node_count, node_name_list = node_name_list, username = session['username'], usertype = session['usertype'])
    else:
        return redirect(url_for('login'))

# Show node
@app.route('/node/<node_name>')
def showNode(node_name):
    if session.get('logged_in'):
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        return jsonify( process_info = Node(node_config).process_dict) 
    else:
        return redirect(url_for('login'))

@app.route('/node/<node_name>/process/<process_name>/restart')
def json_restart(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 'Admin' or session['usertype'] == 'Standart User':
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                if node.connection.supervisor.stopProcess(process_name):
                    if node.connection.supervisor.startProcess(process_name):
                        return JsonValue(process_name, node_name, "restart").success()
            except xmlrpclib.Fault as err:
                return JsonValue(process_name, node_name, "restart").error(err.faultCode, err.faultString)
        else:
            return jsonify(status = "error2",
                           message = "You are not authorized this action" )
    else:
        return redirect(url_for('login'))

# Process start
@app.route('/node/<node_name>/process/<process_name>/start')
def json_start(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 'Admin' or session['usertype'] == 'Standart User':
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                if node.connection.supervisor.startProcess(process_name):
                    return JsonValue(process_name, node_name, "start").success()
            except xmlrpclib.Fault as err:
                return JsonValue(process_name, node_name, "start").error(err.faultCode, err.faultString)
        else:   
            return jsonify(status = "error2",
                           message = "You are not authorized this action" )
    else:
        return redirect(url_for('login'))

# Process stop
@app.route('/node/<node_name>/process/<process_name>/stop')
def json_stop(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 'Admin' or session['usertype'] == 'Standart User':
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                if node.connection.supervisor.stopProcess(process_name):
                    return JsonValue(process_name, node_name, "stop").success()
            except xmlrpclib.Fault as err:
                return JsonValue(process_name, node_name, "stop").error(err.faultCode, err.faultString)
        else:
            return jsonify(status = "error2",
                           message = "You are not authorized this action" )
    else:
        return redirect(url_for('login'))

# Node name list in the configuration file
@app.route('/node/name/list')
def getlist():
    if session.get('logged_in'):
        node_name_list = []
        node_names = Config(CONFIG_FILE).getAllNodeNames()
        for node_name in node_names:
            node_name_list.append(node_name[5:])
        return jsonify( node_name_list = node_name_list )
    else:
        return redirect(url_for('login'))

# Show log for process
@app.route('/node/<node_name>/process/<process_name>/readlog')
def readlog(node_name, process_name):
    node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
    node = Node(node_config)
    log = node.connection.supervisor.tailProcessStdoutLog(process_name, 0, 500)[0]
    return jsonify(url="node/"+node_name+"/process/"+process_name+"/read" , log=log)
     
    

# Add user method for only admin type user
@app.route('/add/user')
def add_user():
    if session.get('logged_in'):
        if session['usertype'] == 'Admin':
            return jsonify(status = 'success')
        else:
            return jsonify(status = 'error')


# Delete user method for only admin type user
@app.route('/delete/user')
def del_user():
    if session.get('logged_in'):
        if session['usertype'] == 'Admin':
            cur = get_db().cursor()
            cur.execute("select username from userinfo")
            usernames = cur.fetchall();
            usernamelist =[str(element[0]) for element in usernames]
            cur.execute("select type from userinfo")
            usertypes = cur.fetchall();
            usertypelist =[str(element[0]) for element in usertypes]
            return jsonify(status = 'success',
                           names = usernamelist,
                           types = usertypelist)
        else:
            return jsonify(status = 'error')

@app.route('/delete/user/<username>')
def del_user_handler(username):
    if session.get('logged_in'):
        if session['usertype'] == 'Admin':
            if username != "admin":
                cur = get_db().cursor()
                cur.execute("delete from userinfo where username=?",[username])
                get_db().commit()
                return jsonify(status = "success")
            else:
                return jsonify(status = "error",
                               message= "Admin can't delete")
        else:
            return jsonify(status = "error",
                           message = "Only Admin can delete a user")
    else:
        return redirect(url_for('login'))

# Writes new user information to database
@app.route('/add/user/handler', methods = ['GET', 'POST'])
def adduserhandler():
    username = request.form['username']
    password = request.form['password']
    usertype = request.form['usertype']
    cur = get_db().cursor()
    cur.execute("select * from userinfo where username=?",(username,))
    if not cur.fetchall():
        cur.execute("insert into userinfo values(?, ?, ?)", (username, password, usertype,))
        get_db().commit()
        return redirect(url_for('showMain'))
    else:
        return redirect(url_for('add_user'))

@app.route('/change/password/<username>')
def changepassword(username):
    return jsonify(status = "success")


@app.route('/change/password/<username>/handler', methods=['GET', 'POST'])
def changepasswordhandler(username):
    if request.method == 'POST':
        cur = get_db().cursor()
        cur.execute("select password from userinfo where username=?",(username,))
        ar=[str(r[0]) for r in cur.fetchall()]
        if request.form['old'] == ar[0]:
            if request.form['new'] == request.form['confirm']:
                cur.execute("update userinfo set password=? where username=?",[request.form['new'], username])
                get_db().commit()
                return jsonify(status = "success")
            return jsonify(status = "error", message = "Passwords do not match")
        return jsonify(status = "error", message = "Old password is wrong")
    else:
        return "  "

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
