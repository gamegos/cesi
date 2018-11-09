import sys
import configparser

from flask import abort
import tomlkit
from tomlkit.toml_file import TOMLFile

from .node import Node
from models import User
from run import db

CESI_CONF_SCHEMA = {
    "cesi": {"database", "activity_log", "admin_username", "admin_password"},
    "nodes": {"name", "host", "port", "username", "password", "environment"},
}


class Cesi:
    __instance = None
    __config_file_path = None

    def __init__(self, config_file_path):
        if Cesi.__instance != None:
            raise Exception(
                "This class is a singleton! Once you need to create a cesi object."
            )

        print("Parsing config file...")
        Cesi.__config_file_path = config_file_path
        self.load_config()
        Cesi.__instance = self

    @staticmethod
    def getInstance():
        """ Static access method """
        if Cesi.__instance == None:
            raise Exception(
                "This class is a singleton! First you must create a cesi object."
            )

        return Cesi.__instance

    def __getattr__(self, name):
        if name in self.__cesi.keys():
            return self.__cesi[name]
        else:
            raise AttributeError

    def _check_config_file(self, config):
        for section_name, section_value in config.items():
            if section_name == "cesi":
                if not set(section_value) == CESI_CONF_SCHEMA[section_name]:
                    sys.exit(
                        "Failed to read {0} configuration file. Problem is the cesi section.".format(
                            Cesi.__config_file_path
                        )
                    )
            elif section_name == "nodes":
                for node in section_value:
                    if not set(node) == CESI_CONF_SCHEMA[section_name]:
                        sys.exit(
                            "Failed to read {0} configuration file. Problem is the nodes section".format(
                                Cesi.__config_file_path
                            )
                        )
            else:
                sys.exit(
                    "Failed to read {0} configuration file. Unknown '{1}' section name".format(
                        Cesi.__config_file_path, section_name
                    )
                )

        return True

    def parse_config_file(self):
        try:
            config = TOMLFile(Cesi.__config_file_path).read()
        except Exception as e:
            sys.exit(
                "Failed to open/find {0} file. {1}".format(Cesi.__config_file_path, e)
            )

        self._check_config_file(config)
        self.__cesi = config.get("cesi", None)
        if self.__cesi is None:
            sys.exit(
                "Failed to read {0} configuration file. You must write cesi section.".format(
                    Cesi.__config_file_path
                )
            )
        self.nodes = []

        for node in config.get("nodes", []):
            _environment = node["environment"] or "default"
            _node = Node(
                name=node["name"],
                environment=_environment,
                host=node["host"],
                port=node["port"],
                username=node["username"],
                password=node["password"],
            )
            self.nodes.append(_node)

    def load_config(self):
        self.parse_config_file()

    def reload(self):
        print("Reloading...")
        self.load_config()
        print("Reloaded.")

    def check_database(self):
        try:
            ### Create Tables
            db.create_all()
            ### Add Admin User
            admin_user = User.register(username="admin", password="admin", usertype=0)
        except Exception as e:
            print(e)

    def get_all_processes(self):
        processes = []
        for n in self.nodes:
            if n.is_connected:
                for p in n.processes:
                    p.dictionary["node"] = n.name
                    p.dictionary["environment"] = n.environment
                    processes.append(p)

            else:
                print(
                    "{} is not connected for get_all_processes() operation.".format(
                        n.name
                    )
                )

        return processes

    def get_groups(self):
        groups = dict()
        for p in self.get_all_processes():
            groups[p.group] = groups.get(p.group, dict())
            group = groups[p.group]
            group[p.environment] = group.get(p.environment, [])
            if p.node not in groups[p.group][p.environment]:
                groups[p.group][p.environment].append(p.node)

        print("Groups: ", groups)
        return groups

    def get_groups_tree(self):
        result = []
        for group_name, environments in self.get_groups().items():
            group = dict()
            group["name"] = group_name
            group["environments"] = []
            for environment_name, members in environments.items():
                environment = dict(name=environment_name, members=members)
                group["environments"].append(environment)

            result.append(group)

        print("GroupsTree: {}".format(result))
        return result

    def get_node(self, node_name):
        for n in self.nodes:
            if n.name == node_name:
                return n

        return None

    def get_node_or_400(self, node_name):
        _node = self.get_node(node_name)
        if _node is None:
            abort(400, description="Wrong node name")

        return _node

    def serialize_nodes(self):
        return [n.serialize() for n in self.nodes]

    def get_environment_names(self):
        environment_names = set()
        for n in self.nodes:
            environment_names.add(n.environment)

        return list(environment_names)

    def get_nodes_by_environment(self, environment_name):
        nodes = []
        for n in self.nodes:
            if n.environment == environment_name:
                nodes.append(n.serialize())

        return nodes

    def get_environment_details(self, environment_name):
        environment = {
            "name": environment_name,
            "members": self.get_nodes_by_environment(environment_name),
        }
        return environment

    def serialize_environments(self):
        environments_with_details = []
        for environment_name in self.get_environment_names():
            environment_detail = self.get_environment_details(environment_name)
            environments_with_details.append(environment_detail)

        return environments_with_details
