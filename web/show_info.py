import os
from flask import Flask, render_template
import getProcInfo 
from getProcInfo import Config
import xmlrpclib

app = Flask(__name__)
app.config.from_object(__name__)

address="http://%s:%s@%s:%s/RPC2" %(Config.username, Config.password, Config.host, Config.port)
server = xmlrpclib.Server(address)

@app.route('/')
def show_info():
    info_list = []
    lis = server.supervisor.getAllProcessInfo()
    for i in lis:
        one = getProcInfo.ProcInfo(i)
        info_list.append(one)
    return render_template('show_info.html', info_list = info_list)

@app.route('/process/<event>')
def action(event):
    if event == "restart":
#        <?php $proc_name = _POST['restart'] ?>
        server.supervisor.stopProcess(proc_name)
        server.supervisor.startProcess(proc_name)
        
    if event == "stop":
#        <?php $proc_name = _POST['stop'] ?>
        server.supervisor.stopProcess(proc_name)




if __name__ == '__main__':
    app.run()
