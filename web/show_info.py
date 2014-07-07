import os
import sys
sys.path.append("../lib")
from flask import Flask, render_template
import getProcInfo 

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def show_info():
    obj = getProcInfo.Proc_info("long5_script")
    name = obj.name
    group = obj.group
    start = obj.start
    stop = obj.stop
    now = obj.now
    state = obj.state
    statename = obj.statename
    spawnerr = obj.spawnerr
    exitstatus = obj.exitstatus
    stdoutlog = obj.stdout_logfile
    stderrlog = obj.stderr_logfile
    pid = obj.pid
    info_list = (name, group, start, stop, now, state, statename, spawnerr, exitstatus, stdoutlog, stderrlog, pid)
    return render_template('layout.html', info_list=info_list)
            
           # name=name, group=group, start=start, stop=stop,\
           # now=now, state=state, statename=statename, spawnerr=spawnerr, exitstatus=exitstatus,\
           # stdoutlog=stdoutlog, stderrlog=stderrlog, pid=pid)

if __name__ == '__main__':
    app.run()
