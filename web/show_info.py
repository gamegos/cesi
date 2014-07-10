from flask import Flask, render_template, url_for, redirect
from getProcInfo import Config, Connection, Node
import getProcInfo 
import xmlrpclib

app = Flask(__name__)
app.config.from_object(__name__)

connection = Connection(Config('DEFAULT').host, Config('DEFAULT').port, Config('DEFAULT').username, Config('DEFAULT').password).getConnection()

@app.route('/')
def show_info():
    info_list = []
    lis = connection.supervisor.getAllProcessInfo()
    for i in lis:
        one = getProcInfo.ProcessInfo(i)
        info_list.append(one)
    return render_template('show_info.html', info_list = info_list)

@app.route('/node/<node_name>')
def nodelist(node_name):
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
