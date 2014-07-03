class Proc_info:
    import xmlrpclib
    server = xmlrpclib.Server('http://user:123@gulsah.game.gos:9001/RPC2')

    def __init__(self, process_name):
        self.process_name = process_name
        self.process_info = Proc_info.server.supervisor.getProcessInfo(process_name)
        self.name = self.process_info['name']

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


one = Proc_info("long5_script")

print one.name
