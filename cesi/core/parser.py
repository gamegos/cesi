import sys

import tomlkit
from tomlkit.toml_file import TOMLFile

from .node import Node

CESI_CONF_SCHEMA = {
    "cesi": {"database", "activity_log", "admin_username", "admin_password"},
    "nodes": {"name", "host", "port", "username", "password", "environment"},
}


def read_config_file(config_file_path):
    try:
        config = TOMLFile(config_file_path).read()
    except Exception as e:
        sys.exit("Failed to open/find {0} file. {1}".format(config_file_path, e))

    return config


# TODO:: Refactor this function.
def check_config_file(config_file_path):
    configurations = read_config_file(config_file_path)
    for section_name, section_value in configurations.items():
        if section_name == "cesi":
            if not set(section_value) == CESI_CONF_SCHEMA[section_name]:
                sys.exit(
                    "Failed to read '{0}' configuration file. Problem is the cesi section.".format(
                        config_file_path
                    )
                )
        elif section_name == "nodes":
            for node in section_value:
                if not set(node) == CESI_CONF_SCHEMA[section_name]:
                    sys.exit(
                        "Failed to read '{0}' configuration file. Problem is the nodes section".format(
                            config_file_path
                        )
                    )
        else:
            sys.exit(
                "Failed to read {0} configuration file. Unknown '{1}' section name".format(
                    config_file_path, section_name
                )
            )

    field_name = "cesi"
    _field = configurations.get(field_name, None)
    if _field is None:
        sys.exit(
            "Failed to read '{0}' configuration file. You must write '{1}' section.".format(
                config_file_path, field_name
            )
        )

    return configurations


def parse_config_file(config_file_path):
    configurations = check_config_file(config_file_path)

    result = {}
    nodes = []
    node_environments = set()
    node_names = set()
    for field in CESI_CONF_SCHEMA["cesi"]:
        result[field] = configurations["cesi"][field]

    for node in configurations.get("nodes", []):
        node_name = node["name"]
        node_environment = node.get("environment", "default")
        node_names.add(node_name)
        node_environments.add(node_environment)

        _node = Node(
            name=node_name,
            environment=node_environment,
            host=node["host"],
            port=node["port"],
            username=node["username"],
            password=node["password"],
        )
        nodes.append(_node)

    result["nodes"] = nodes
    result["node_environments"] = node_environments
    result["node_names"] = node_names
    return result

