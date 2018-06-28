import xmlrpc.client

from flask import abort
from .xmlrpc import XmlRpc
from .process import Process

class Node:
    def __init__(self, name, host, port, username, password):
        self.name = name
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = XmlRpc.connection(self.host, self.port, self.username, self.password)

    @property
    def processes(self):
        _processes = []
        try:
            for p in self.connection.supervisor.getAllProcessInfo():
                _process = Process(p)
                _processes.append(_process)

            return _processes
        
        except Exception as _:
            return []

    @property
    def is_connected(self):
        return self.__connect()

    def __connect(self):
        if self.connection:
            try:
                self.connection.system.listMethods()
                print(f"Yes, node connected. {self.name}")
                return True
            except (xmlrpc.client.ProtocolError, xmlrpc.client.Fault, Exception) as e:
                print(e)
    
        print(f"No, node isn't connected. {self.name}")
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
        __processes = []
        for p in self.processes:
            if p.group == group_name:
                __processes.append(p)

        return __processes

    def start_process(self, process_name):
        """ http://supervisord.org/api.html#supervisor.rpcinterface.SupervisorNamespaceRPCInterface.startProcess """
        process = self.get_process_or_400(process_name)
        try:
            if self.connection.supervisor.startProcess(process.name):
                return True, ""
            else:
                return False, "cannot start process"
        except xmlrpc.client.Fault as err:
            return False, err.faultString

    def stop_process(self, process_name):
        process = self.get_process_or_400(process_name)
        try:
            if self.connection.supervisor.stopProcess(process.name):
                return True, ""
            else:
                return False, "aaaa"
        except xmlrpc.client.Fault as err:
            return False, err.faultString

    def restart_process(self, process_name):
        process = self.get_process_or_400(process_name)
        if process.state == 20:
            status, msg = self.stop_process(process_name)
            if not status:
                return status, msg
        
        return self.start_process(process_name)

    def serialize_general(self):
        return {
            'name': self.name,
            'host': self.host,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'connected': self.is_connected
        }

    def serialize_processes(self):
        return {
            'processes': [p.serialize() for p in self.processes],
        }

    def serialize(self):
        _serialized_general = self.serialize_general()
        _serialized_processes = self.serialize_processes()
        return dict(_serialized_general, **_serialized_processes)

    def full_name(self):
        return f"node:{self.name}"