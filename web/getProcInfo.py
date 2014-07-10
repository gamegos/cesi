import xmlrpclib
import ConfigParser

CFILE = "/etc/supervisor-centralized.conf"

class Config:
    
    def __init__(self, CFILE):
        self.CFILE = CFILE
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(self.CFILE)
        
    def getSectionName(self, section_name):
        self.section_name = "node:%s" % (section_name)
        self.username = self.cfg.get(self.section_name, 'username')
        self.password = self.cfg.get(self.section_name, 'password')
        self.host = self.cfg.get(self.section_name, 'host')
        self.port = self.cfg.get(self.section_name, 'port')

    def allSectionsName(self):
        self.slist = self.cfg.sections()
        return self.slist
            
class Node:

    def __init__(self, name):
        self.name = name
        self.config = Config(CFILE).getSectionName(self.name)
        self.connection = Connection(self.config.host, self.config.port, self.config.username, self.config.password).getConnection()
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


#class SupervisorInfo:

#    def __init__(self):
#        self.cfg = Config(CFILE).getSectionName('node:gulsah')
#        self.connection = Connection(self.cfg.host, self.cfg.port, self.cfg.username, self.cfg.password)
#        self.api_version = self.connection.supervisor.getAPIVersion()
#        self.supervisor_version = self.connection.supervisor.getSupervisorVersion()
#        self.supervisor_id = self.connection.supervisor.getIdentification()
#        self.state_code = self.connection.supervisor.getState()['statecode']
#        self.state_name = self.connection.supervisor.getState()['statename']
#        self.pid= self.connection.supervisor.getPID()

#    def readLog(self,offset,length):
#        self.offset = offset
#        self.length = length
#        self.log = Supervisord_info.connection.supervisor.readLog(offset,length)
#        return self.log

#    def clearLog(self):
#        if(Supervisord_info.connection.supervisor.clearLog()):
#            return "Cleared supervisosd main log"
#        return "Could not cleared log"

#    def shutdown(self):
#        if(Supervisord_info.state_code == 1):
#            Supervisord_info.connection.supervisor.shutdown()
#            return "Success shutdown"
#        else:
#            return "Unsuccess shutdown"
    
#    def restart(self):
#        if(Supervisord_info.state_code == 1):
#            Supervisord_info.connection.supervisor.restart()
#            return "Success restart"
#        else:
#            return "Unsuccess restart"

