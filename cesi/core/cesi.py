import sys
import sqlite3
import configparser

from flask import abort

from .node import Node
from .environment import Environment

class Cesi:
    """ Cesi """
    __instance = None
    __config_file_path = None
    __defaults = {
        'host': 'localhost',
        'port': '5000',
        'name': 'CeSI',
        'theme': 'superhero',
        'activity_log': '/var/logs/cesi/activity.log',
        'database': 'userinfo.db',
        'debug': 'True',
        'secret_key': 'lalalala',
        'auto_reload': 'True',
        'default_user': 'admin',
        'default_password': 'admin',
    }
    
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

        print("Parsing config file...")
        Cesi.__config_file_path = config_file_path
        self.load_config()
        self.check_database()
        Cesi.__instance = self
    
    def drop_database(self):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("""DROP TABLE userinfo""")
        conn.commit()
        conn.close()

    def check_database(self):
        conn = self.get_db_connection()
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
        self.__cesi = Cesi.__defaults
        self.nodes = []
        self.environments = []

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
            else:
                print(f"Unknowed section name: {section.name}")

        self.fill_defaults_environment()

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

    @property
    def groups(self):
        result = {}
        for node in self.nodes:
            if node.is_connected:
                for p in node.processes:
                    result[p.group] = result.get(p.group, [])
                    if node.name not in result[p.group]:
                        result[p.group].append(node.name)
            else:
                print(f"{node.name} is not connected.")

        print(result)
        return result

    def get_groups_tree(self):
        __groups = self.groups
        __result = {}
        for env in self.environments:
            print(env.name)
            for group_name, node_names in __groups.items():
                __result[group_name] = __result.get(group_name, {})
                for node_name in node_names:
                    environment = self.get_environment_by_node_name(node_name)
                    if environment:
                        __result[group_name][environment.name] = __result[group_name].get(environment.name, [])
                        if node_name not in __result[group_name][environment.name]:
                            __result[group_name][environment.name].append(node_name)

        print(__result)
        return __result

    def get_db_connection(self):
        try:
            conn = sqlite3.connect(self.database)
            return conn
        except Exception as e:
            sys.exit(e)

    def get_node(self, node_name):
        _nodes_iterator = filter(lambda n: n.name == node_name, self.nodes)
        return next(_nodes_iterator, None)

    def get_node_or_400(self, node_name):
        _node = self.get_node(node_name)
        if _node is None:
            abort(400, description="Wrong node name")
        
        return _node

    def fill_defaults_environment(self):
        # fill defaults
        empty_nodes = []
        for node in self.nodes:
            _environment = self.get_environment_by_node_name(node.name)
            if not _environment:
                empty_nodes.append(node.name)

        environment = Environment(name="defaults")
        environment.set_members(empty_nodes)
        self.environments.append(environment)

    def get_environment(self, environment_name):
        _environment = filter(lambda e: e.name == environment_name, self.environments)
        return next(_environment, None)

    def get_environment_or_400(self, environment_name):
        _environment = self.get_environment(environment_name)
        if _environment is None:
            abort(400, description="Wrong environment name")
        
        return _environment

    def get_environment_by_node_name(self, node_name):
        _environment = filter(lambda e: node_name in e.members, self.environments)
        return next(_environment, None)

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