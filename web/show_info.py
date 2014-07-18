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
        return render_template('index.html', node_list = node_list)
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
        return render_template('index.html', node_list = node_list)
    except xmlrpclib.Fault as err:
        print "A fault occurred"
        print "Fault code: %d" % err.faultCode
        print "Fault string: %s" % err.faultString

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
