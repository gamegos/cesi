class Proc_info:
    import xmlrpclib
    server = xmlrpclib.Server('http://user:123@gulsah.game.gos:9001/RPC2')

    def __init__(self, process_name):
        self.process_name = process_name
        self.process_info = Proc_info.server.supervisor.getProcessInfo(process_name)
        self.name = self.process_info['name']
	self.group = self.process_info['group']
	self.start = self.process_info['start']
	self.stop = self.process_info['stop']
	self.now = self.process_info['now']
	self.state = self.process_info['state']
	self.statename = self.process_info['statename']
	self.spawnerr = self.process_info['spawnerr']
	self.exitstatus = self.process_info['exitstatus']
	self.stdout_logfile = self.process_info['stdout_logfile']
	self.stderr_logfile = self.process_info['stderr_logfile']
	self.pid = self.process_info['pid']


one = Proc_info("long5_script")

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
