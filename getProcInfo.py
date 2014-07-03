class Proc_info:
	import xmlrpclib
	server = xmlrpclib.Server('http://user:123@localhost:9001/RPC2')

	def __init__(self, process_name):
		self.process_name =	process_name
		process_info=		Proc_info.server.supervisor.getProcessInfo(process_name)
		name = 			process_info('name')
		group = 		process_info('group')
		start = 		process_info('start')
		stop = 			process_info('stop')
		now = 			process_info('now')
		state = 		process_info('state')
		statename = 		process_info('statename')
		spawnerr = 		process_info('spawnerr')
		exitstatus = 		process_info('exitstatus')
		stdout_logfile = 	process_info('stdout_logfile')
		stderr_logfile = 	process_info('stderr_logfile')
		pid = 			process_info('pid')
	
	def get_name(self):
		return self.name

	def get_group(self):
		return group

	def get_start():
		return start

	def get_stop():
		return stop
	
	def get_now():
		return now

	def get_state():
		return state

	def get_statename():
		return statename
	
	def get_spawnerr():
		return spawnerr

	def exitstatus():
		return exitstatus
	
	def stdout_logfile():
		return stdout_logfile
	
	def stderr_logfile():
		return stderr_logfile

	def get_pid():
		return pid

one = Proc_info("long5_script")

print one.get_name()
