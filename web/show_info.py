from flask import Flask, render_template, url_for, redirect, jsonify
from getProcInfo import Config, Connection, Node, CONFIG_FILE, ProcessInfo, JsonValue
import getProcInfo 
import xmlrpclib

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def showAllProcess():
    try:
        node_list = []
        node_names = Config(CONFIG_FILE).getAllNodeNames()
        for node_name in node_names:
            node_name = node_name[5:]
            node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
            node = Node(node_config)
            node_list.append(node) 
        return render_template('show_info.html', node_list = node_list)
    except xmlrpclib.Fault as err:
        print "A fault occurred"
        print "Fault code: %d" % err.faultCode
        print "Fault string: %s" % err.faultString

@app.route('/node/<node_name>')
def showNode(node_name):
    try:
        node_list=[]
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        node_list.append(node)
        return render_template('show_info.html', node_list = node_list)
    except xmlrpclib.Fault as err:
        print "A fault occurred"
        print "Fault code: %d" % err.faultCode
        print "Fault string: %s" % err.faultString

@app.route('/node/<node_name>/process/stop/<process_name>')
def stopProcess(node_name, process_name):
    try:
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        node.connection.supervisor.stopProcess(process_name)
        return redirect(url_for('showNode', node_name = node_name)) 
    except xmlrpclib.Fault as err:
        print "A fault occurred"
        print "Fault code: %d" % err.faultCode
        print "Fault string: %s" % err.faultString

@app.route('/node/<node_name>/process/start/<process_name>')
def startProcess(node_name, process_name):
    try:
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        node.connection.supervisor.startProcess(process_name)
        return redirect(url_for('showNode', node_name = node_name)) 
    except xmlrpclib.Fault as err:
        print "A fault occurred"
        print "Fault code: %d" % err.faultCode
        print "Fault string: %s" % err.faultString

@app.route('/node/<node_name>/process/restart/<process_name>')
def restartProcess(node_name, process_name):
    try:
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        node.connection.supervisor.stopProcess(process_name)
        node.connection.supervisor.startProcess(process_name)
        return redirect(url_for('showNode', node_name = node_name)) 
    except xmlrpclib.Fault as err:
        print "A fault occurred"
        print "Fault code: %d" % err.faultCode
        print "Fault string: %s" % err.faultString

@app.route('/node/all/<node_name>/process/stop/<process_name>')
def stopProcessFromAll(node_name, process_name):
    try:
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        node.connection.supervisor.stopProcess(process_name)
        return redirect(url_for('showAllProcess', node_name = node_name)) 
    except xmlrpclib.Fault as err:
        print "A fault occurred"
        print "Fault code: %d" % err.faultCode
        print "Fault string: %s" % err.faultString

@app.route('/node/all/<node_name>/process/start/<process_name>')
def startProcessFromAll(node_name, process_name):
    try:
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        node.connection.supervisor.startProcess(process_name)
        return redirect(url_for('showAllProcess', node_name = node_name)) 
    except xmlrpclib.Fault as err:
        print "A fault occurred"
        print "Fault code: %d" % err.faultCode
        print "Fault string: %s" % err.faultString

@app.route('/node/all/<node_name>/process/restart/<process_name>')
def restartProcessFromAll(node_name, process_name):
    try:
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        node.connection.supervisor.stopProcess(process_name)
        node.connection.supervisor.startProcess(process_name)
        return redirect(url_for('showAllProcess', node_name = node_name)) 
    except xmlrpclib.Fault as err:
        print "A fault occurred"
        print "Fault code: %d" % err.faultCode
        print "Fault string: %s" % err.faultString

@app.route('/environment/node/<node_name>/process/start/<process_name>')
@app.route('/environment/node/all/<node_name>/process/start/<process_name>')
def startProcessJson(node_name, process_name):
    try:
        dict_array_process_info=[]
        status={}
        code={}
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        if node.connection.supervisor.startProcess(process_name):
            return JsonValue(process_name, node_name, "start").success()
        else:
            return jsonify(status = "Error",
                           code = "Unknown")
    except xmlrpclib.Fault as err:
        print "A fault occurred"
        print "Fault code: %d" % err.faultCode
        print "Fault string: %s" % err.faultString


@app.route('/environment/node/<node_name>/process/stop/<process_name>')
@app.route('/environment/node/all/<node_name>/process/stop/<process_name>')
def stopProcessJson(node_name, process_name):
    try:
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        if node.connection.supervisor.stopProcess(process_name):
            return JsonValue(process_name, node_name, "stop").success()
        else:
            return jsonify(status = "Error",
                           code = "Unknown")
    except xmlrpclib.Fault as err:
        print "A fault occurred"
        print "Fault code: %d" % err.faultCode
        print "Fault string: %s" % err.faultString


@app.route('/environment/node/<node_name>/process/restart/<process_name>')
@app.route('/environment/node/all/<node_name>/process/restart/<process_name>')
def restartProcessJson(node_name, process_name):
    try:
        array_process_info=[]
        status={}
        code={}
        node_config = Config(CONFIG_FILE).getNodeConfig(node_name)
        node = Node(node_config)
        if node.connection.supervisor.stopProcess(process_name):
            if node.connection.supervisor.startProcess(process_name):
                return JsonValue(process_name, node_name, "restart").success()
        else:
            return jsonify(status = "Error",
                           code = "Unknown")
    except xmlrpclib.Fault as err:
        print "A fault occurred"
        print "Fault code: %d" % err.faultCode
        print "Fault string: %s" % err.faultString

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
