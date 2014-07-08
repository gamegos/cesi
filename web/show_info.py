import os
import sys
from flask import Flask, render_template
import getProcInfo 
import ConfigParser
import xmlrpclib

CFILE = "/etc/supervisord-centralized.conf"

app = Flask(__name__)
app.config.from_object(__name__)

cfg = ConfigParser.ConfigParser()
cfg.read(CFILE)
user = cfg.get('DEFAULT', 'user')
password = cfg.get('DEFAULT', 'password')
host = cfg.get('DEFAULT', 'host')
port = cfg.get('DEFAULT', 'port')
address="http://%s:%s@%s:%s/RPC2" %(user, password, host, port)
server = xmlrpclib.Server(address)
lis = server.supervisor.getAllProcessInfo()
info_list = []

@app.route('/')
def show_info():
    lis = server.supervisor.getAllProcessInfo()
    for i in lis:
        one = getProcInfo.Proc_info(i)
        info_list.append(one)
    return render_template('show_info.html', info_list = info_list)
            
           # name=name, group=group, start=start, stop=stop,\
           # now=now, state=state, statename=statename, spawnerr=spawnerr, exitstatus=exitstatus,\
           # stdoutlog=stdoutlog, stderrlog=stderrlog, pid=pid)

if __name__ == '__main__':
    app.run()
