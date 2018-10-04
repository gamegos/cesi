import xmlrpc.client

from flask import abort
from .xmlrpc import XmlRpc
from .process import Process


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
        if self.connection:
            try:
                self.connection.system.listMethods()
                print("Yes, node connected. {}".format(self.name))
                return True
            except (xmlrpc.client.ProtocolError, xmlrpc.client.Fault) as err:
                print(err)
            except Exception as err:
                print(err)

        print("No, node isn't connected. {}".format(self.name))
        return False

    def get_process(self, process_name):
        try:
            _p = self.connection.supervisor.getProcessInfo(process_name)
            return Process(_p)
        except Exception as err:
            print(err)
            return None

    def get_process_or_400(self, process_name):
        process = self.get_process(process_name)
        if not process:
            return abort(400, description="Wrong process name")

        return process

    def get_processes_by_group_name(self, group_name):
        return [p for p in self.processes if p.group == group_name]

    def start_process(self, process_name):
        """
            http://supervisord.org/api.html#supervisor.rpcinterface.SupervisorNamespaceRPCInterface.startProcess
        """
        process = self.get_process_or_400(process_name)
        try:
            if self.connection.supervisor.startProcess(process.name):
                return True, ""
            else:
                return False, "cannot start process"
        except xmlrpc.client.Fault as err:
            return False, err.faultString
        except Exception as err:
            return False, str(err)

    def stop_process(self, process_name):
        process = self.get_process_or_400(process_name)
        try:
            if self.connection.supervisor.stopProcess(process.name):
                return True, ""
            else:
                return False, "cannot stop process"
        except xmlrpc.client.Fault as err:
            return False, err.faultString
        except Exception as err:
            return False, str(err)

    def restart_process(self, process_name):
        process = self.get_process_or_400(process_name)
        if process.state == 20:
            status, msg = self.stop_process(process_name)
            if not status:
                return status, msg

        return self.start_process(process_name)

    def serialize_general(self):
        return {
            "name": self.name,
            "environment": self.environment,
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
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
