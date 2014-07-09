import xmlrpclib
import ConfigParser

class Config:
    CFILE = "/etc/supervisor-centralized.conf"
    cfg = ConfigParser.ConfigParser()
    cfg.read(CFILE)
    username = cfg.get('DEFAULT', 'user')
    password = cfg.get('DEFAULT', 'password')
    host = cfg.get('DEFAULT', 'host')
    port = cfg.get('DEFAULT', 'port')


class Connection:

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.address = "http://%s:%s@%s:%s/RPC2" %(self.username, self.password, self.host, self.port)

    def getConnection(self):
        return xmlrpclib.Server(self.address)
        

class ProcInfo:

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


class SupervisorInfo:

    connection = Connection(Config.host, Config.port, Config.username, Config.password).getConnection()
    api_version = connection.supervisor.getAPIVersion()
    supervisor_version = connection.supervisor.getSupervisorVersion()
    supervisor_id = version = connection.supervisor.getIdentification()
    state_code = connection.supervisor.getState()['statecode']
    state_name = connection.supervisor.getState()['statename']
    pid= connection.supervisor.getPID()

    def readLog(self,offset,length):
        self.offset = offset
        self.length = length
        self.log = Supervisord_info.connection.supervisor.readLog(offset,length)
        return self.log

    def clearLog(self):
        if(Supervisord_info.connection.supervisor.clearLog()):
            return "Cleared supervisosd main log"
        return "Could not cleared log"

    def shutdown(self):
        if(Supervisord_info.state_code == 1):
            Supervisord_info.connection.supervisor.shutdown()
            return "Success shutdown"
        else:
            return "Unsuccess shutdown"
    
    def restart(self):
        if(Supervisord_info.state_code == 1):
            Supervisord_info.connection.supervisor.restart()
            return "Success restart"
        else:
            return "Unsuccess restart"

