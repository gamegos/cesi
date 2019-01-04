import xmlrpc.client

from flask import abort

from .xmlrpc import XmlRpc
from .process import Process
from .handlers import xmlrpc_exceptions


class Node:
    def __init__(self, name, environment, host, port, username, password):
        self.name = name
        self.environment = environment
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = XmlRpc.connection(
            self.host, self.port, self.username, self.password
        )

    @property
    def processes(self):
        try:
            return [
                Process(_p) for _p in self.connection.supervisor.getAllProcessInfo()
            ]
        except Exception as _:
            return []

    @property
    def is_connected(self):
        return self.__connect()

    def __connect(self):
        status, msg = self.get_system_list_methods_for_xmlrpc_server()
        if not status:
            print("Node: '{}', Error: '{}'".format(self.name, msg))
        return status

    @xmlrpc_exceptions
    def get_system_list_methods_for_xmlrpc_server(self):
        self.connection.system.listMethods()
        return True, "Okey, got system list methods"

    @xmlrpc_exceptions
    def get_process(self, unique_name):
        _p = self.connection.supervisor.getProcessInfo(unique_name)
        return Process(_p), ""

    def get_process_or_400(self, unique_name):
        process, msg = self.get_process(unique_name)
        if not process:
            return abort(400, description="Wrong process name")

        return process

    def get_process_logs(self, unique_name):
        stdout_log_string = self.connection.supervisor.tailProcessStdoutLog(
            unique_name, 0, 500
        )[0]
        stderr_log_string = self.connection.supervisor.tailProcessStderrLog(
            unique_name, 0, 500
        )[0]
        logs = {
            "stdout": stdout_log_string.split("\n")[1:-1],
            "stderr": stderr_log_string.split("\n")[1:-1],
        }
        return logs

    def get_processes_by_group_name(self, group_name):
        return [p for p in self.processes if p.group == group_name]

    @xmlrpc_exceptions
    def start_process(self, unique_name):
        if self.connection.supervisor.startProcess(unique_name):
            return True, ""
        else:
            return False, "cannot start process"

    @xmlrpc_exceptions
    def stop_process(self, unique_name):
        if self.connection.supervisor.stopProcess(unique_name):
            return True, ""
        else:
            return False, "cannot stop process"

    def restart_process(self, unique_name):
        process = self.get_process_or_400(unique_name)
        if process.state == 20:
            status, msg = self.stop_process(unique_name)
            if not status:
                return status, msg

        return self.start_process(unique_name)

    def serialize_general(self):
        return {
            "name": self.name,
            "environment": self.environment,
            # "host": self.host,
            # "port": self.port,
            # "username": self.username,
            # "password": self.password,
            "connected": self.is_connected,
        }

    def serialize_processes(self):
        return [p.serialize() for p in self.processes]

    def serialize(self):
        _serialized_general = self.serialize_general()
        _serialized_processes = self.serialize_processes()
        return {
            "general": self.serialize_general(),
            "processes": self.serialize_processes(),
        }

    def full_name(self):
        return "node:{}".format(self.name)
