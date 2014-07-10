from flask import Flask, render_template, url_for, redirect
from getProcInfo import Config, Connection, Node
import getProcInfo 
import xmlrpclib

app = Flask(__name__)
app.config.from_object(__name__)

CFILE="/etc/supervisor-centralized.conf"

@app.route('/')
def showAllProcess():
    node_list = []
    node_names = Config(CFILE).getAllNodeNames()
    for node_name in node_names:
        node_name = node_name[5:]
        node_config = Config(CFILE).getNodeConfig(node_name)
        node = Node(node_config)
        node_list.append(node)

    for node in node_list:
        for process in node.process_list:
            print node.name, process.name

    return ""
    



    #process_list=[]
    #for node_name in Config(CFILE).allSectionsName():
    #    node_name = node_name[5:]
    #    process_list.append(Node(node_name).process_list)
    #return render_template('show_info.html', process_list = plist)

@app.route('/node/<node_name>')
def showNode(node_name):
    node = Node(node_name)
    return render_template('show_info.html', process_list = node.process_list, node_name = node_name)

@app.route('/node/<node_name>/process/stop/<process_name>')
def stopProcess(node_name, process_name):
    Node(node_name).connection.supervisor.stopProcess(process_name)
    return redirect(url_for('nodelist', node_name = node_name)) 

@app.route('/node/<node_name>/process/start/<process_name>')
def startProcess(node_name, process_name):
    Node(node_name).connection.supervisor.startProcess(process_name)
    return redirect(url_for('nodelist', node_name = node_name)) 

@app.route('/node/<node_name>/process/restart/<process_name>')
def restartProcess(node_name, process_name):
    Node(node_name).connection.supervisor.stopProcess(process_name)
    Node(node_name).connection.supervisor.startProcess(process_name)
    return redirect(url_for('nodelist', node_name = node_name)) 

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
