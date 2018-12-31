from flask import abort

from .parser import parse_config_file


class Cesi:
    __instance = None
    __config_file_path = None

    def __init__(self, config_file_path):
        if Cesi.__instance != None:
            raise Exception(
                "This class is a singleton! Once you need to create a cesi object."
            )

        Cesi.__config_file_path = config_file_path

        self.config_file_path = config_file_path
        self.database = "sqlite:///users.db"
        self.activity_log = "activity.log"
        self.admin_username = "admin"
        self.admin_password = "admin"
        self.node_names = tuple()
        self.node_environments = set()
        self.nodes = list()

        self.load()

        Cesi.__instance = self

    @staticmethod
    def getInstance():
        """ Static access method """
        if Cesi.__instance == None:
            raise Exception(
                "This class is a singleton! First you must create a cesi object."
            )

        return Cesi.__instance

    def load(self):
        print("Loading config file...")
        result = parse_config_file(self.config_file_path)
        self.database = result["database"]
        self.activity_log = result["activity_log"]
        self.admin_username = result["admin_username"]
        self.admin_password = result["admin_password"]
        self.node_names = result["node_names"]
        self.node_environments = result["node_environments"]
        self.nodes = result["nodes"]
        print(result)

    def reload(self):
        print("Reloading...")
        self.load()
        print("Reloaded.")

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
        for environment_name in self.node_environments:
            environment_detail = self.get_environment_details(environment_name)
            environments_with_details.append(environment_detail)

        return environments_with_details
