from flask import Flask, render_template, url_for, redirect, jsonify, request, g, session, flash
from getProcInfo import Config, Connection, Node, CONFIG_FILE, CONFIG_FILE2, ProcessInfo, JsonValue
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
            session.clear()
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
                session.clear()
                return "Invalid password"

# Render login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')

# Logout action
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard
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
     
        all_process_count = 0
        running_process_count = 0
        stopped_process_count = 0
        member_names = []
        environment_list = []

        node_name_list = Config(CONFIG_FILE).node_list
        node_count = len(node_name_list)
        environment_name_list = Config(CONFIG_FILE).environment_list
        
        for nodename in node_name_list:
            nodeconfig = Config(CONFIG_FILE).getNodeConfig(nodename)
            node = Node(nodeconfig)
            for process in node.process_list:
                all_process_count = all_process_count + 1
                if process.state==20:
                    running_process_count = running_process_count + 1
                if process.state==0:
                    stopped_process_count = stopped_process_count + 1

        # get environment list 
        for env_name in environment_name_list:
            env_name = Config(CONFIG_FILE).getMemberNames(env_name)
            environment_list.append(env_name)

        return render_template('index.html',
                                all_process_count =all_process_count,
                                running_process_count =running_process_count,
                                stopped_process_count =stopped_process_count,
                                node_count =node_count,
                                node_name_list = node_name_list,
                                environment_list = environment_list,
                                environment_name_list = environment_name_list,
                                group_list = group_list,
                                username = session['username'],
                                usertype = usertype)
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
        if session['usertype'] == 0 or session['usertype'] == 1:
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
        if session['usertype'] == 0 or session['usertype'] == 1:
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
        if session['usertype'] == 0 or session['usertype'] == 1:
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
        node_name_list = Config(CONFIG_FILE).node_list
        return jsonify( node_name_list = node_name_list )
    else:
        return redirect(url_for('login'))

# Show log for process
@app.route('/node/<node_name>/process/<process_name>/readlog')
def readlog(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1 or session['usertype'] == 2:
            node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
            node = Node(node_config)
            log = node.connection.supervisor.tailProcessStdoutLog(process_name, 0, 500)[0]
            return jsonify( status = "success", url="node/"+node_name+"/process/"+process_name+"/read" , log=log)
        else:
            return jsonify( status = "error", message= "You are not authorized for this action")
    else:
        return jsonify( status = "error", message= "First login please")

# Add user method for only admin type user
@app.route('/add/user')
def add_user():
    if session.get('logged_in'):
        if session['usertype'] == 0:
            return jsonify(status = 'success')
        else:
            return jsonify(status = 'error')


# Delete user method for only admin type user
@app.route('/delete/user')
def del_user():
    if session.get('logged_in'):
        if session['usertype'] == 0:
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
        if session['usertype'] == 0:
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
    if session.get('logged_in'):
        if session['usertype'] == 0:
            username = request.form['username']
            password = request.form['password']
            confirmpassword = request.form['confirmpassword']

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
                    return jsonify(status = "success",
                                   message ="User added")
                else:
                    return jsonify(status = "error",
                                   message ="Passwords didn't match")
            else:
                return jsonify(status = "error",
                               message ="Username is avaible. Please select different username")
        else:
            return jsonify(status = "error",
                           message = "Only Admin can delete a user")
    else:
        return jsonify(status = "error",
                       message = "First login please")



@app.route('/change/password/<username>')
def changepassword(username):
    if session.get('logged_in'):
        if session['username'] == username:
            return jsonify(status = "success")
        else:
            return jsonify(status = "error",
                           message = "You can only change own password.")
    else:
        return redirect(url_for('login'))



@app.route('/change/password/<username>/handler', methods=['POST'])
def changepasswordhandler(username):
    if session.get('logged_in'):
        if session['username'] == username:
            cur = get_db().cursor()
            cur.execute("select password from userinfo where username=?",(username,))
            ar=[str(r[0]) for r in cur.fetchall()]
            if request.form['old'] == ar[0]:
                if request.form['new'] == request.form['confirm']:
                    cur.execute("update userinfo set password=? where username=?",[request.form['new'], username])
                    get_db().commit()
                    return jsonify(status = "success")
                else:
                    return jsonify(status = "error", message = "Passwords do not match")
            else:
                return jsonify(status = "error", message = "Old password is wrong")
        else:
            return jsonify(status = "error", message = "You can only change own password.")
    else:
        return redirect(url_for('login'))

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
