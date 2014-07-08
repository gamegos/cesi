import os
from flask import Flask, render_template
import getProcInfo 
import xmlrpclib

app = Flask(__name__)
app.config.from_object(__name__)

address="http://%s:%s@%s:%s/RPC2" %(getProcInfo.Parser.user, getProcInfo.Parser.password, getProcInfo.Parser.host, getProcInfo.Parser.port)
server = xmlrpclib.Server(address)

@app.route('/')
def show_info():
    info_list = []
    lis = server.supervisor.getAllProcessInfo()
    for i in lis:
        one = getProcInfo.ProcInfo(i)
        info_list.append(one)
    return render_template('show_info.html', info_list = info_list)

if __name__ == '__main__':
    app.run()
