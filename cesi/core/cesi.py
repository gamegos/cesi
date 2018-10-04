import sys
import sqlite3
import configparser

from flask import abort

from .node import Node


class Cesi:
    """ Cesi """

    __instance = None
    __config_file_path = None
    __necessaries = {
        "cesi": {
            "fields": [
                "host",
                "port",
                "name",
                "theme",
                "activity_log",
                "database",
                "debug",
                "auto_reload",
                "admin_username",
                "admin_password",
            ],
            "boolean_fields": ["debug", "auto_reload"],
        },
        "node": {"fields": ["host", "port", "username", "password", "environment"]},
    }

    @staticmethod
    def getInstance():
        """ Static access method """
        if Cesi.__instance == None:
            raise Exception(
                "This class is a singleton! First you must create a cesi object."
            )

        return Cesi.__instance

    def __init__(self, config_file_path):
        """ Config File Parsing"""
        if Cesi.__instance != None:
            raise Exception(
                "This class is a singleton! Once you need to create a cesi object."
            )

        print("Parsing config file...")
        Cesi.__config_file_path = config_file_path
        self.load_config()
        Cesi.__instance = self

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
        sql_insert_admin_user = """insert into userinfo values('{username}', '{password}', 0);""".format(
            username=self.admin_username, password=self.admin_password
        )
        try:
            cur.execute(sql_insert_admin_user)
            conn.commit()
        except Exception as e:
            print(e)

        conn.close()

    def __check_config_file(self, config):
        for section_name in config.sections():
            section = config[section_name]
            if section.name == "cesi":
                for field in self.__necessaries["cesi"]["fields"]:
                    value = section.get(field, None)
                    if value is None:
                        sys.exit(
                            "Failed to read {0} file, Not found '{1}' field in Cesi section.".format(
                                Cesi.__config_file_path, field
                            )
                        )

                    # Checking boolean field
                    if field in self.__necessaries["cesi"]["boolean_fields"]:
                        if not value in ["True", "False"]:
                            sys.exit(
                                "Failed to read {0} file, '{1}' field is not True or False.".format(
                                    Cesi.__config_file_path, field
                                )
                            )

            elif section.name[:4] == "node":
                # 'node:<name>'
                clean_name = section.name[5:]
                for field in self.__necessaries["node"]["fields"]:
                    value = section.get(field, None)
                    if value is None:
                        sys.exit(
                            "Failed to read {0} file, Not found '{1}' field in '{2}' node section.".format(
                                Cesi.__config_file_path, field, clean_name
                            )
                        )

            else:
                sys.exit(
                    "Failed to open/find {0} file, Unknowed section name: '{1}'".format(
                        Cesi.__config_file_path, section.name
                    )
                )

    def reload(self):
        print("Reloading...")
        self.load_config()
        print("Reloaded.")

    def load_config(self):
        self.parse_config()
        self.check_database()

    def parse_config(self):
        self.__cesi = {}
        self.nodes = []

        config = configparser.ConfigParser()
        dataset = config.read(Cesi.__config_file_path)
        if dataset == []:
            sys.exit("Failed to open/find {0} file".format(Cesi.__config_file_path))

        self.__check_config_file(config)

        for section_name in config.sections():
            section = config[section_name]
            if section.name == "cesi":
                for field in self.__necessaries["cesi"]["fields"]:
                    value = section.get(field)
                    if field in self.__necessaries["cesi"]["boolean_fields"]:
                        value = True if value == "True" else False

                    self.__cesi[field] = value

            elif section.name[:4] == "node":
                # 'node:<name>'
                clean_name = section.name[5:]
                environment = section.get("environment")
                if environment == "":
                    environment = "defaults"

                _node = Node(
                    name=clean_name,
                    environment=environment,
                    host=section.get("host"),
                    port=section.get("port"),
                    username=section.get("username"),
                    password=section.get("password"),
                )
                self.nodes.append(_node)
            else:
                pass

    def __getattr__(self, name):
        if name in self.__cesi.keys():
            return self.__cesi[name]
        else:
            raise AttributeError

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

    def get_db_connection(self):
        try:
            conn = sqlite3.connect(self.database)
            return conn
        except Exception as e:
            sys.exit(e)

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
            "nodes": self.get_nodes_by_environment(environment_name),
        }
        return environment

    def serialize_environments(self):
        environments_with_details = []
        for environment_name in self.get_environment_names():
            environment_detail = self.get_environment_details(environment_name)
            environments_with_details.append(environment_detail)

        return environments_with_details
