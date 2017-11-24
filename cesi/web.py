from flask import Flask, render_template, url_for, redirect, jsonify, request, g, session, flash
from cesi import Config, Connection, Node, CONFIG_FILE, ProcessInfo, JsonValue
from datetime import datetime
import cesi 
import xmlrpclib
import sqlite3
import mmap
import os
import time

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key= '42'

DATABASE = Config(CONFIG_FILE).getDatabase()
ACTIVITY_LOG = Config(CONFIG_FILE).getActivityLog()
HOST = Config(CONFIG_FILE).getHost()

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

@app.route('/activitylog')
def getlogtail():
    n=12
    try:
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
        return jsonify(status = "success",
                       log = lines)
    except Exception as err:
        return jsonify(status = "error",
                       messagge= err)
    finally:
        try:
            fm.close()
        except (UnboundLocalError, TypeError):
            return jsonify(status="error",
                           message = "Activity log file is empty")
            



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
    return render_template('login.html', code=code)

# Logout action
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    add_log = open(ACTIVITY_LOG, "a")
    add_log.write("%s - %s logged out.\n"%( datetime.now().ctime(), session['username'] ))
    session.clear()
    return redirect('/login')

# User Info
@app.route('/userinfo')
def userInfo():
   if session.get('logged_in'):
       return jsonify(username = session['username'],usertypecode = session['usertype'])
   else:
      return jsonify(message = 'Session expired'), 403

# Dashboard
@app.route('/dashboard')
def showInfo():
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
        g_node_list = []
        g_process_list = []
        g_environment_list = []
        group_list = []
        not_connected_node_list = []
        connected_node_list = []

        node_name_list = Config(CONFIG_FILE).node_list
        node_count = len(node_name_list)
        environment_name_list = Config(CONFIG_FILE).environment_list

        for nodename in node_name_list:
            nodeconfig = Config(CONFIG_FILE).getNodeConfig(nodename)

            try:
                node = Node(nodeconfig)
                if not nodename in connected_node_list:
                    connected_node_list.append(nodename);
            except Exception as err:
                 if not nodename in not_connected_node_list:
                    not_connected_node_list.append(nodename);
                 continue

            for name in node.process_dict2.keys():
                p_group = name.split(':')[0]
                p_name = name.split(':')[1]
                if p_group != p_name:
                    if not p_group in group_list:
                        group_list.append(p_group)

            for process in node.process_list:
                all_process_count = all_process_count + 1
                if process.state==20:
                    running_process_count = running_process_count + 1
                if process.state==0:
                    stopped_process_count = stopped_process_count + 1 

        # get environment list 
        for env_name in environment_name_list:
            env_members = Config(CONFIG_FILE).getMemberNames(env_name)
            for index, node in enumerate(env_members):
                if not node in connected_node_list:
                    env_members.pop(index);
            environment_list.append(env_members)        
                    
        
        for g_name in group_list:
            tmp= []
            for nodename in connected_node_list:
                nodeconfig = Config(CONFIG_FILE).getNodeConfig(nodename)
                node = Node(nodeconfig)
                for name in node.process_dict2.keys():
                    group_name = name.split(':')[0]
                    if group_name == g_name:
                        if not nodename in tmp:
                            tmp.append(nodename)
            g_node_list.append(tmp)

        for sublist in g_node_list:
            tmp = []
            for name in sublist:
                for env_name in environment_name_list:
                    if name in Config(CONFIG_FILE).getMemberNames(env_name):
                        if name in connected_node_list:
                            if not env_name in tmp:
                                tmp.append(env_name)
            g_environment_list.append(tmp)
        
        connected_count = len(connected_node_list)
        not_connected_count = len(not_connected_node_list)

        return jsonify(			all_process_count =all_process_count,
                                running_process_count =running_process_count,
                                stopped_process_count =stopped_process_count,
                                node_count =node_count,
                                node_name_list = node_name_list,
                                connected_count = connected_count,
                                not_connected_count = not_connected_count,
                                environment_list = environment_list,
                                environment_name_list = environment_name_list,
                                group_list = group_list,
                                g_environment_list = g_environment_list,
                                connected_node_list = connected_node_list,
                                not_connected_node_list = not_connected_node_list,
                                username = session['username'],
                                usertype = usertype,
                                usertypecode = session['usertype'])
    else:   
        return jsonify(message = 'Session expired'), 403

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
        g_node_list = []
        g_process_list = []
        g_environment_list = []
        group_list = []
        not_connected_node_list = []
        connected_node_list = []

        node_name_list = Config(CONFIG_FILE).node_list
        node_count = len(node_name_list)
        environment_name_list = Config(CONFIG_FILE).environment_list
        
        

        for nodename in node_name_list:
            nodeconfig = Config(CONFIG_FILE).getNodeConfig(nodename)

            try:
                node = Node(nodeconfig)
                if not nodename in connected_node_list:
                    connected_node_list.append(nodename);
            except Exception as err:
                 if not nodename in not_connected_node_list:
                    not_connected_node_list.append(nodename);
                 continue



            for name in node.process_dict2.keys():
                p_group = name.split(':')[0]
                p_name = name.split(':')[1]
                if p_group != p_name:
                    if not p_group in group_list:
                        group_list.append(p_group)

            for process in node.process_list:
                all_process_count = all_process_count + 1
                if process.state==20:
                    running_process_count = running_process_count + 1
                if process.state==0:
                    stopped_process_count = stopped_process_count + 1

        
    
        # get environment list 
        for env_name in environment_name_list:
            env_members = Config(CONFIG_FILE).getMemberNames(env_name)
            for index, node in enumerate(env_members):
                if not node in connected_node_list:
                    env_members.pop(index);
            environment_list.append(env_members)        
                    
        
        for g_name in group_list:
            tmp= []
            for nodename in connected_node_list:
                nodeconfig = Config(CONFIG_FILE).getNodeConfig(nodename)
                node = Node(nodeconfig)
                for name in node.process_dict2.keys():
                    group_name = name.split(':')[0]
                    if group_name == g_name:
                        if not nodename in tmp:
                            tmp.append(nodename)
            g_node_list.append(tmp)

        for sublist in g_node_list:
            tmp = []
            for name in sublist:
                for env_name in environment_name_list:
                    if name in Config(CONFIG_FILE).getMemberNames(env_name):
                        if name in connected_node_list:
                            if not env_name in tmp:
                                tmp.append(env_name)
            g_environment_list.append(tmp)
        
        connected_count = len(connected_node_list)
        not_connected_count = len(not_connected_node_list)

        return render_template('index.html',
                                name = Config(CONFIG_FILE).getName(),
                                theme = Config(CONFIG_FILE).getTheme(),
                                all_process_count =all_process_count,
                                running_process_count =running_process_count,
                                stopped_process_count =stopped_process_count,
                                node_count =node_count,
                                node_name_list = node_name_list,
                                connected_count = connected_count,
                                not_connected_count = not_connected_count,
                                environment_list = environment_list,
                                environment_name_list = environment_name_list,
                                group_list = group_list,
                                g_environment_list = g_environment_list,
                                connected_node_list = connected_node_list,
                                not_connected_node_list = not_connected_node_list,
                                username = session['username'],
                                usertype = usertype,
                                usertypecode = session['usertype'])
    else:   
         return redirect('/login')


# Show node
@app.route('/node/<node_name>')
def showNode(node_name):
    if session.get('logged_in'):
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - %s viewed node %s .\n"%( datetime.now().ctime(), session['username'], node_name ))
        return jsonify( process_info = Node(node_config).process_dict) 
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for view node %s .\n"%( datetime.now().ctime(), node_name ))
        return jsonify(message = 'Session expired'), 403



@app.route('/node/all/start')
def startAll():
    if session.get('logged_in'):
        node_name_list = Config(CONFIG_FILE).node_list
        for nodename in node_name_list:
            nodeconfig = Config(CONFIG_FILE).getNodeConfig(nodename)

            try:
                node = Node(nodeconfig)
            except Exception as err:
                continue

            for process in node.process_list:
                json_start(nodename, process.name)
                
        return jsonify(status="success")
    else:
        return jsonify(message = 'Session expired'), 403



@app.route('/node/all/stop')
def stopAll():
    if session.get('logged_in'):
        node_name_list = Config(CONFIG_FILE).node_list
        for nodename in node_name_list:
            nodeconfig = Config(CONFIG_FILE).getNodeConfig(nodename)

            try:
                node = Node(nodeconfig)
            except Exception as err:
                continue

            for process in node.process_list:
                json_stop(nodename, process.name)

        return jsonify(status="success")
    else:
        return jsonify(message = 'Session expired'), 403

@app.route('/node/all/restart')
def restartAll():
    if session.get('logged_in'):
        node_name_list = Config(CONFIG_FILE).node_list
        for nodename in node_name_list:
            nodeconfig = Config(CONFIG_FILE).getNodeConfig(nodename)

            try:
                node = Node(nodeconfig)
            except Exception as err:
                continue

            for process in node.process_list:
                json_restart(nodename, process.name)
                
        return jsonify(status="success")
    else:
        return jsonify(message = 'Session expired'), 403

@app.route('/group/<group_name>/environment/<environment_name>')
def showGroup(group_name, environment_name):
    if session.get('logged_in'):
        env_memberlist = Config(CONFIG_FILE).getMemberNames(environment_name)
        process_list = []
        for nodename in env_memberlist:
            node_config = Config(CONFIG_FILE).getNodeConfig(nodename)
            try:
                node = Node(node_config)
            except Exception as err:
                continue
            p_list = node.process_dict2.keys()
            for name in p_list:
                if name.split(':')[0] == group_name:
                    tmp = []
                    tmp.append(node.process_dict2[name].pid)
                    tmp.append(name.split(':')[1])
                    tmp.append(nodename)
                    tmp.append(node.process_dict2[name].uptime)
                    tmp.append(node.process_dict2[name].state)
                    tmp.append(node.process_dict2[name].statename)
                    process_list.append(tmp)
        return jsonify(process_list = process_list)
    else:
        return jsonify(message = 'Session expired'), 403


@app.route('/node/<node_name>/process/<process_name>/restart')
def json_restart(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1:
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                if node.connection.supervisor.stopProcess(process_name):
                    if node.connection.supervisor.startProcess(process_name):
                        add_log = open(ACTIVITY_LOG, "a")
                        add_log.write("%s - %s restarted %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
                        return JsonValue(process_name, node_name, "restart").success()
            except xmlrpclib.Fault as err:
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s unsucces restart event %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
                return JsonValue(process_name, node_name, "restart").error(err.faultCode, err.faultString)
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for restart. Restart event fail for %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
            return jsonify(status = "error2",
                           message = "You are not authorized this action" )
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for restart to %s node's %s process %s .\n"%( datetime.now().ctime(), node_name, process_name ))
        return jsonify(message = 'Session expired'), 403

# Process start
@app.route('/node/<node_name>/process/<process_name>/start')
def json_start(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1:
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                if node.connection.supervisor.startProcess(process_name):
                    add_log = open(ACTIVITY_LOG, "a")
                    add_log.write("%s - %s started %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
                    return JsonValue(process_name, node_name, "start").success()
                else:
                    return jsonify(status="error1",
                               message="Cannot start process")
            except xmlrpclib.Fault as err:
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s unsucces start event %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
                return JsonValue(process_name, node_name, "start").error(err.faultCode, err.faultString)
        else:   
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for start. Start event fail for %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
            return jsonify(status = "error2",
                           message = "You are not authorized this action" )
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for start to %s node's %s process %s .\n"%( datetime.now().ctime(), node_name, process_name ))
        return jsonify(message = 'Session expired'), 403

# Process stop
@app.route('/node/<node_name>/process/<process_name>/stop')
def json_stop(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1:
            try:
                node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
                node = Node(node_config)
                if node.connection.supervisor.stopProcess(process_name):
                    add_log = open(ACTIVITY_LOG, "a")
                    add_log.write("%s - %s stopped %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
                    return JsonValue(process_name, node_name, "stop").success()
                else:
                    return jsonify(status="error1",
                               message="Cannot stop process")
            except xmlrpclib.Fault as err:
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s unsucces stop event %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
                return JsonValue(process_name, node_name, "stop").error(err.faultCode, err.faultString)
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for stop. Stop event fail for %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
            return jsonify(status = "error2",
                           message = "You are not authorized this action" )
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for stop to %s node's %s process %s .\n"%( datetime.now().ctime(), node_name, process_name ))
        return jsonify(message = 'Session expired'), 403

# Node name list in the configuration file
@app.route('/node/name/list')
def getlist():
    if session.get('logged_in'):
        node_name_list = Config(CONFIG_FILE).node_list
        return jsonify( node_name_list = node_name_list )
    else:
        return jsonify(message = 'Session expired'), 403

# Show log for process
@app.route('/node/<node_name>/process/<process_name>/readlog')
def readlog(node_name, process_name):
    if session.get('logged_in'):
        if session['usertype'] == 0 or session['usertype'] == 1 or session['usertype'] == 2:
            node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
            node = Node(node_config)
            log = node.connection.supervisor.tailProcessStdoutLog(process_name, 0, 500)[0]
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s read log %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
            return jsonify( status = "success", url="node/"+node_name+"/process/"+process_name+"/read" , log=log)
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user request for read log. Read log event fail for %s node's %s process .\n"%( datetime.now().ctime(), session['username'], node_name, process_name ))
            return jsonify( status = "error", message= "You are not authorized for this action")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for read log to %s node's %s process %s .\n"%( datetime.now().ctime(), node_name, process_name ))
        return jsonify( status = "error", message= "First login please")

# Add user method for only admin type user
@app.route('/add/user')
def add_user():
    if session.get('logged_in'):
        if session['usertype'] == 0:
            return jsonify(status = 'success')
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - Unauthorized user request for add user event. Add user event fail .\n"%( datetime.now().ctime() ))
            return jsonify(status = 'error')


# Delete user method for only admin type user
@app.route('/delete/user')
def del_user():
    if session.get('logged_in'):
        if session['usertype'] == 0:
            cur = get_db().cursor()
            cur.execute("select username, type from userinfo")
            users = cur.fetchall();
            usernamelist =[str(element[0]) for element in users]
            usertypelist =[str(element[1]) for element in users]
            return jsonify(status = 'success',
                           names = usernamelist,
                           types = usertypelist)
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - Unauthorized user request for delete user event. Delete user event fail .\n"%( datetime.now().ctime() ))
            return jsonify(status = 'error')

@app.route('/delete/user/<username>')
def del_user_handler(username):
    if session.get('logged_in'):
        if session['usertype'] == 0:
            if username != "admin":
                cur = get_db().cursor()
                cur.execute("delete from userinfo where username=?",[username])
                get_db().commit()
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s user deleted .\n"%( datetime.now().ctime(), username ))
                return jsonify(status = "success")
            else:
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s  user request for delete admin user. Delete admin user event fail .\n"%( datetime.now().ctime(), session['username'] ))
                return jsonify(status = "error",
                               message= "Admin can't delete")
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user for request to delete a user. Delete event fail .\n"%( datetime.now().ctime(), session['username'] ))
            return jsonify(status = "error",
                           message = "Only Admin can delete a user")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for delete user event.\n"%( datetime.now().ctime()))
        return jsonify(message = 'Session expired'), 403

# Writes new user information to database
@app.route('/add/user/handler', methods = ['GET', 'POST'])
def adduserhandler():
    if session.get('logged_in'):
        if session['usertype'] == 0:
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
                        add_log = open(ACTIVITY_LOG, "a")
                        add_log.write("%s - New user added.\n"%( datetime.now().ctime() ))
                        return jsonify(status = "success",
                                       message ="User added")
                    else:
                        add_log = open(ACTIVITY_LOG, "a")
                        add_log.write("%s - Passwords didn't match at add user event.\n"%( datetime.now().ctime() ))
                        return jsonify(status = "warning",
                                       message ="Passwords didn't match")
                else:
                    add_log = open(ACTIVITY_LOG, "a")
                    add_log.write("%s - Username is avaible at add user event.\n"%( datetime.now().ctime() ))
                    return jsonify(status = "warning",
                                   message ="Username is avaible. Please select different username")
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user for request to add user event. Add user event fail .\n"%( datetime.now().ctime(), session['username'] ))
            return jsonify(status = "error",
                           message = "Only Admin can add a user")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for add user event.\n"%( datetime.now().ctime()))
        return jsonify(status = "error",
                       message = "First login please")



@app.route('/change/password/<username>')
def changepassword(username):
    if session.get('logged_in'):
        if session['username'] == username:
            return jsonify(status = "success")
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s user request to change %s 's password. Change password event fail\n"%( datetime.now().ctime(), session['username'], username))
            return jsonify(status = "error",
                           message = "You can only change own password.")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for change %s 's password event.\n"%( datetime.now().ctime(), username))
        return jsonify(message = 'Session expired'), 403



@app.route('/change/password/<username>/handler', methods=['POST'])
def changepasswordhandler(username):
    if session.get('logged_in'):
        if session['username'] == username:
            cur = get_db().cursor()
            cur.execute("select password from userinfo where username=?",(username,))
            ar=[str(r[0]) for r in cur.fetchall()]
            if request.form['old'] == ar[0]:
                if request.form['new'] == request.form['confirm']:
                    if request.form['new'] != "":
                        cur.execute("update userinfo set password=? where username=?",[request.form['new'], username])
                        get_db().commit()
                        add_log = open(ACTIVITY_LOG, "a")
                        add_log.write("%s - %s user change own password.\n"%( datetime.now().ctime(), session['username']))
                        return jsonify(status = "success")
                    else:
                        return jsonify(status = "null",
                                       message = "Please enter valid value")
                else:
                    add_log = open(ACTIVITY_LOG, "a")
                    add_log.write("%s - Passwords didn't match for %s 's change password event. Change password event fail .\n"%( datetime.now().ctime(), session['username']))
                    return jsonify(status = "error", message = "Passwords didn't match")
            else:
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - Old password is wrong for %s 's change password event. Change password event fail .\n"%( datetime.now().ctime(), session['username']))
                return jsonify(status = "error", message = "Old password is wrong")
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s user request to change %s 's password. Change password event fail\n"%( datetime.now().ctime(), session['username'], username))
            return jsonify(status = "error", message = "You can only change own password.")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for change %s 's password event.\n"%( datetime.now().ctime(), username))
        return jsonify(message = 'Session expired'), 403

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
