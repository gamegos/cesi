import xmlrpclib
import ConfigParser

CONFIG_FILE = "/etc/supervisor-centralized.conf"

class Config:
    
    def __init__(self, CFILE):
        self.CFILE = CFILE
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(self.CFILE)
        
    def getNodeConfig(self, node_name):
        self.node_name = "node:%s" % (node_name)
        self.username = self.cfg.get(self.node_name, 'username')
        self.password = self.cfg.get(self.node_name, 'password')
        self.host = self.cfg.get(self.node_name, 'host')
        self.port = self.cfg.get(self.node_name, 'port')
        self.node_config = NodeConfig(self.node_name, self.host, self.port, self.username, self.password)
        return self.node_config

    def getAllNodeNames(self):
        node_list = self.cfg.sections()
        return node_list


class NodeConfig:

        def __init__(self, node_name, host, port, username, password):
            self.node_name = node_name
            self.host = host
            self.port = port
            self.username = username
            self.password = password
            

class Node:

    def __init__(self, node_config):
        self.name = node_config.node_name
        self.connection = Connection(node_config.host, node_config.port, node_config.username, node_config.password).getConnection()
        self.process_list = []
        for p in self.connection.supervisor.getAllProcessInfo():
            self.process_list.append(ProcessInfo(p))

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
        self.stop = self.dictionary['stop']
        self.now = self.dictionary['now']
        self.state = self.dictionary['state']
        self.statename = self.dictionary['statename']
        self.spawnerr = self.dictionary['spawnerr']
        self.exitstatus = self.dictionary['exitstatus']
        self.stdout_logfile = self.dictionary['stdout_logfile']
        self.stderr_logfile = self.dictionary['stderr_logfile']
        self.pid = self.dictionary['pid']


