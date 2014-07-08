import xmlrpclib
import ConfigParser

CFILE = "/etc/supervisord-centralized.conf"

class Proc_info:

    cfg = ConfigParser.ConfigParser()
    cfg.read(CFILE)
    user = cfg.get('DEFAULT', 'user')
    password = cfg.get('DEFAULT', 'password')
    host = cfg.get('DEFAULT', 'host')
    port = cfg.get('DEFAULT', 'port')
    address="http://%s:%s@%s:%s/RPC2" %(user, password, host, port)
    server = xmlrpclib.Server(address)

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


class Supervisord_info:

    cfg = ConfigParser.ConfigParser()
    cfg.read(CFILE)
    user = cfg.get('DEFAULT', 'user')
    password = cfg.get('DEFAULT', 'password')
    host = cfg.get('DEFAULT', 'host')
    port = cfg.get('DEFAULT', 'port')
    address="http://%s:%s@%s:%s/RPC2" %(user, password, host, port)
    server = xmlrpclib.Server(address)

    api_version = server.supervisor.getAPIVersion()
    supervisor_version = server.supervisor.getSupervisorVersion()
    supervisor_id = version = server.supervisor.getIdentification()
    state_code = server.supervisor.getState()['statecode']
    state_name = server.supervisor.getState()['statename']
    pid= server.supervisor.getPID()

    def readlog(self,offset,length):
        self.offset = offset
        self.length = length
        self.log = Supervisord_info.server.supervisor.readLog(offset,length)
        return self.log

    def clearlog(self):
        if(Supervisord_info.server.supervisor.clearLog()):
            return "Cleared supervisosd main log"
        return "Could not cleared log"

    def shutdown(self):
        if(Supervisord_info.state_code == 1):
            Supervisord_info.server.supervisor.shutdown()
            return "Success shutdown"
        else:
            return "Unsuccess shutdown"
    
    def restart(self):
        if(Supervisord_info.state_code == 1):
            Supervisord_info.server.supervisor.restart()
            return "Success restart"
        else:
            return "Unsuccess restart"

print "*****************Supervisor Control******************************"
print Supervisord_info.api_version
print Supervisord_info.supervisor_version
print Supervisord_info.supervisor_id
print Supervisord_info.state_code
print Supervisord_info.state_name

two = Supervisord_info()
print two.readlog(1,10)
print two.clearlog()
#print two.restart()
#print two.shutdown()


print "****************Process Control*******************************"

cfg = ConfigParser.ConfigParser()
cfg.read(CFILE)
user = cfg.get('DEFAULT', 'user')
password = cfg.get('DEFAULT', 'password')
host = cfg.get('DEFAULT', 'host')
port = cfg.get('DEFAULT', 'port')
address="http://%s:%s@%s:%s/RPC2" %(user, password, host, port)
server = xmlrpclib.Server(address)

lis = server.supervisor.getAllProcessInfo()
for i in lis:
    one = Proc_info(i)
    print "Name= %s" % (one.name)
    print "Group= %s" % (one.group)
    print "Start= %s" % (one.start)
    print "Stop= %s" % (one.stop)
    print "Now= %s" % (one.now)
    print "State= %s" % (one.state)
    print "Statename= %s" % (one.statename)
    print "Spawnerr= %s" % (one.spawnerr)
    print "Exitstatus= %s" % (one.exitstatus)
    print "Stdout_logfile= %s" % (one.stdout_logfile)
    print "Stderr_logfile= %s" % (one.stderr_logfile)
    print "Pid= %s" % (one.pid)

