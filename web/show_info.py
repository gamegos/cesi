from flask import Flask, render_template, url_for, redirect
from getProcInfo import Config, Connection
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
        one = getProcInfo.ProcInfo(i)
        info_list.append(one)
    return render_template('show_info.html', info_list = info_list)


@app.route('/process/stop/<process_name>')
def stopProcess(process_name):
    connection.supervisor.stopProcess(process_name)
    return redirect(url_for('show_info')) 

@app.route('/process/start/<process_name>')
def startProcess(process_name):
    connection.supervisor.startProcess(process_name)
    return redirect(url_for('show_info'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
