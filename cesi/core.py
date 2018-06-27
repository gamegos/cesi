import sys
import os.path
import sqlite3
import configparser
import xmlrpc.client
from datetime import datetime, timedelta

from flask import (
    jsonify,
    abort
)

CESI_DEFAULTS = {
    'host': 'localhost',
    'port': '5000',
    'name': 'CeSI',
    'theme': 'superhero',
    'activity_log': '/var/logs/cesi/activity.log',
    'database': 'userinfo.db',
    'debug': 'True',
    'secret_key': 'lalalala',
    'auto_reload': 'True',
}

class Cesi:
    """ Cesi """
    __instance = None
    __config_file_path = None
    
    @staticmethod
    def getInstance():
        """ Static access method """
        if Cesi.__instance == None:
            Cesi()
        return Cesi.__instance

    def __init__(self, config_file_path='/etc/cesi.conf'):
        """ Config File Parsing"""
        if Cesi.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            print("Parsing config file...")
            Cesi.__config_file_path = config_file_path
            # Defaults are problem. Defaults effects all sections.
            self.load_config()
            self.check_database()
            Cesi.__instance = self
    
    def drop_database(self):
        conn = self.get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("""DROP TABLE userinfo""")
            conn.commit()
            conn.close()

    def check_database(self):
        conn = self.get_db_connection()
        if conn:
            print("Connected Database!")
            cur = conn.cursor()
            # Check userinfo table
            sql_create_userinfo_table = """create table if not exists userinfo(
                username varchar(30) PRIMARY KEY NOT NULL,
                password varchar(50) NOT NULL,
                type INT NOT NULL);"""
            cur.execute(sql_create_userinfo_table)
            conn.commit()
            # check admin user.
            sql_insert_admin_user = """insert into userinfo values('admin', 'admin', 0);"""
            try:
                cur.execute(sql_insert_admin_user)
                conn.commit()
            except Exception as e:
                print(e)

            conn.close()

    def load_config(self):
        self.__cesi = CESI_DEFAULTS
        self.nodes = []
        self.environments = []
        self.groups = []

        self.config = configparser.ConfigParser()
        dataset = self.config.read(Cesi.__config_file_path)
        if dataset == []:
            sys.exit(f"Failed to open/find {Cesi.__config_file_path} file")

        for section_name in self.config.sections():
            section = self.config[section_name]
            if section.name == 'cesi':
                # Update cesi configs
                self.__cesi = {
                    'host': section.get('host', self.__cesi['host']),
                    'port': section.get('port', self.__cesi['port']),
                    'name': section.get('name', self.__cesi['name']),
                    'theme': section.get('theme', self.__cesi['theme']),
                    'activity_log': section.get('activity_log', self.__cesi['activity_log']),
                    'database': section.get('database', self.__cesi['database']),
                    'debug': section.get('debug', self.__cesi['debug']),
                    'secret_key': section.get('secret_key', self.__cesi['secret_key']),
                    'auto_reload': section.get('auto_reload', self.__cesi['auto_reload'])
                }
            elif section.name[:4] == 'node':
                # 'node:<name>'
                clean_name = section.name[5:]
                _node = Node(
                    name=clean_name,
                    host=section.get('host'),
                    port=section.get('port'),
                    username=section.get('username'),
                    password=section.get('password'),
                )
                self.nodes.append(_node)
            elif section.name[:11] == 'environment':
                # 'environtment:<name>'
                name = section.name[12:]
                members_string = section.get('members')
                _environment = Environment(
                    name=name,
                    members_string=members_string
                )
                self.environments.append(_environment)
            elif section.name[:5] == 'group':
                # 'group:<name>'
                name = section.name[6:]
                self.groups.append(name[6:])
            else:
                print(f"Unknowed section name: {section.name}")

    @property
    def database(self): return self.__cesi['database']

    @property
    def host(self): return self.__cesi['host']

    @property
    def name(self): return self.__cesi['name']
    
    @property
    def port(self): return self.__cesi['port']
    
    @property
    def theme(self): return self.__cesi['theme']
    
    @property
    def activity_log(self): return self.__cesi['activity_log']

    @property
    def debug(self):
        return True if self.__cesi['debug'] == 'True' else False

    @property
    def auto_reload(self):
        return True if self.__cesi['auto_reload'] == 'True' else False

    @property
    def secret_key(self): return self.__cesi['secret_key']

    def get_db_connection(self):
        try:
            conn = sqlite3.connect(self.database)
            return conn
        except Exception as e:
            sys.exit(e)
        
        return None

    def get_node(self, node_name):
        _nodes_iterator = filter(lambda n: n.name == node_name, self.nodes)
        return next(_nodes_iterator, None)

    def get_node_or_400(self, node_name):
        _node = self.get_node(node_name)
        if _node is None:
            abort(400, description="Wrong node name")
        
        return _node

    def get_environment(self, environment_name):
        _environment = filter(lambda e: e.name == environment_name, self.environments)
        return next(_environment, None)

    def get_environment_or_400(self, environment_name):
        _environment = self.get_environment(environment_name)
        if _environment is None:
            abort(400, description="Wrong environment name")
        
        return _environment

    def serialize_nodes(self):
        return {
            'nodes': [n.serialize() for n in self.nodes],
        }

    def serialize_environments(self):
        return {
            'environments': [e.serialize() for e in self.environments],
        }

    def serialize(self):
        _serialized_nodes = self.serialize_nodes()
        _serialized_environments = self.serialize_environments()
        return dict(_serialized_nodes, **_serialized_environments)

class XmlRpc:
    @staticmethod
    def connection(host, port, username, password):
        if username == "" and password == "":
            address = f"http://{host}:{port}/RPC2"
        else:
            address = f"http://{username}:{password}@{host}:{port}/RPC2"

        try:
            return xmlrpc.client.ServerProxy(address)
        except Exception as e:
            print(e)
            return None

class Process:
    """ Process Class """
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

        self.start_hr = datetime.fromtimestamp(self.start).strftime('%Y-%m-%d %H:%M:%S')[11:]
        self.stop_hr = datetime.fromtimestamp(self.stop).strftime('%Y-%m-%d %H:%M:%S')[11:]
        self.now_hr = datetime.fromtimestamp(self.now).strftime('%Y-%m-%d %H:%M:%S')[11:]
        self.seconds = self.now - self.start
        self.uptime = str(timedelta(seconds=self.seconds))
        self.dictionary.update({
            'start_hr': self.start_hr,
            'stop_hr': self.stop_hr,
            'now_hr': self.now_hr,
            'uptime': self.uptime
        })

    def serialize(self):
        return self.dictionary

class Environment:
    def __init__(self, name, members_string):
        self.name = name
        self.members = list(map(str.strip, members_string.split(',')))

    def serialize(self):
        return {
            'name': self.name,
            'members': self.members
        }

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