import xmlrpclib
import ConfigParser
from datetime import datetime, timedelta
from flask import jsonify



CONFIG_FILE = "/etc/cesi.conf"
class Config:
    DEFAULT_PORT = '5000'
    DEFAULT_NAME = 'CeSI'
    DEFAULT_THEME = 'superhero'

    def __init__(self, CFILE):
        self.CFILE = CFILE
        self.cfg = ConfigParser.SafeConfigParser(defaults={'port': self.DEFAULT_PORT, 'name': self.DEFAULT_NAME, 'theme': self.DEFAULT_THEME})
        self.cfg.read(self.CFILE)

        self.node_list = []
        for name in self.cfg.sections():
            if name[:4] == 'node':
                self.node_list.append(name[5:])

        self.environment_list = []
        for name in self.cfg.sections():
            if name[:11] == 'environment':
                self.environment_list.append(name[12:])

        self.group_list = []
        for name in self.cfg.sections():
            if name[:5] == 'group':
                self.group_list.append(name[6:])

        
    def getNodeConfig(self, node_name):
        self.node_name = "node:%s" % (node_name)
        self.username = self.cfg.get(self.node_name, 'username')
        self.password = self.cfg.get(self.node_name, 'password')
        self.host = self.cfg.get(self.node_name, 'host')
        self.port = self.cfg.get(self.node_name, 'port')
        self.node_config = NodeConfig(self.node_name, self.host, self.port, self.username, self.password)
        return self.node_config

    def getMemberNames(self, environment_name):
        self.environment_name = "environment:%s" % (environment_name)
        self.member_list = self.cfg.get(self.environment_name, 'members')
        self.member_list = self.member_list.split(',')
        self.member_list = map(str.strip, self.member_list)
        return self.member_list

    def getDatabase(self):
        return str(self.cfg.get('cesi', 'database'))

    def getActivityLog(self):
        return str(self.cfg.get('cesi', 'activity_log'))

    def getHost(self):
        return str(self.cfg.get('cesi', 'host'))

    def getPort(self):
        return int(self.cfg.get('cesi', 'port'))

    def getName(self):
        return self.cfg.get('cesi', 'name')

    def getTheme(self):
        return self.cfg.get('cesi', 'theme')


class NodeConfig:

    def __init__(self, node_name, host, port, username, password):
        self.node_name = node_name
        self.host = host
        self.port = port
        self.username = username
        self.password = password
            

class Node:

    def __init__(self, node_config):
        self.long_name = node_config.node_name
        self.name = node_config.node_name[5:]
        self.connection = Connection(node_config.host, node_config.port, node_config.username, node_config.password).getConnection()
        self.process_list=[]
        self.process_dict2={}
        for p in self.connection.supervisor.getAllProcessInfo():
            self.process_list.append(ProcessInfo(p))
            self.process_dict2[p['group']+':'+p['name']] = ProcessInfo(p)
        self.process_dict = self.connection.supervisor.getAllProcessInfo()


class Connection:

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.address = "http://%s:%s@%s:%s/RPC2" %(self.username, self.password, self.host, self.port)

    def getConnection(self):
        return xmlrpclib.Server(self.address)
        

class ProcessInfo:

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.name = self.dictionary['name']
        self.group = self.dictionary['group']
        self.start = self.dictionary['start']
        self.start_hr = datetime.fromtimestamp(self.dictionary['start']).strftime('%Y-%m-%d %H:%M:%S')[11:]
        self.stop_hr = datetime.fromtimestamp(self.dictionary['stop']).strftime('%Y-%m-%d %H:%M:%S')[11:]
        self.now_hr = datetime.fromtimestamp(self.dictionary['now']).strftime('%Y-%m-%d %H:%M:%S')[11:]
        self.stop = self.dictionary['stop']
        self.now = self.dictionary['now']
        self.state = self.dictionary['state']
        self.statename = self.dictionary['statename']
        self.spawnerr = self.dictionary['spawnerr']
        self.exitstatus = self.dictionary['exitstatus']
        self.stdout_logfile = self.dictionary['stdout_logfile']
        self.stderr_logfile = self.dictionary['stderr_logfile']
        self.pid = self.dictionary['pid']
        self.seconds = self.now - self.start
        self.uptime = str(timedelta(seconds=self.seconds))

class JsonValue:
    
    def __init__(self, process_name, node_name, event):
        self.process_name = process_name
        self.event = event
        self.node_name = node_name
        self.node_config = Config(CONFIG_FILE).getNodeConfig(self.node_name)
        self.node = Node(self.node_config)

    def success(self):
        return jsonify(status = "Success",
                       code = 80,
                       message = "%s %s %s event succesfully" %(self.node_name, self.process_name, self.event),
                       nodename = self.node_name,
                       data = self.node.connection.supervisor.getProcessInfo(self.process_name))

    def error(self, code, payload):     
        self.code = code
        self.payload = payload
        return jsonify(status = "Error",
                       code = self.code,
                       message = "%s %s %s event unsuccesful" %(self.node_name, self.process_name, self.event),
                       nodename = self.node_name,
                       payload = self.payload)
