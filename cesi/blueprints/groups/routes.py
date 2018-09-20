from flask import Blueprint, jsonify

from core import Cesi
from loggers import ActivityLog
from decorators import is_user_logged_in, is_admin

groups = Blueprint("groups", __name__)
cesi = Cesi.getInstance()
activity = ActivityLog.getInstance()


@groups.route("/")
@is_user_logged_in()
@is_admin()
def get_groups_tree():
    """
    {
        "groups": {
            "go": {
                "aws": ["ec2-1", "ec2-2"],
                "azure": ["machine-1", "machine-2"],
                "defaults": []
            }
        }
    }
    """
    return jsonify(status="success", result=cesi.get_groups_tree())


@groups.route("/<group_name>/")
@is_user_logged_in()
@is_admin()
def get_group_details(group_name):
    groups = cesi.groups
    group = groups.get(group_name, None)
    if not group:
        return jsonify(status="error", message="Wrong group name"), 400

    result = {}
    for node_name in group:
        n = cesi.get_node(node_name)
        processes = n.get_processes_by_group_name(group_name)
        result[n.name] = []
        for p in processes:
            result[n.name].append(p.serialize())

    print(result)
    return jsonify(status="success", result=result)


@groups.route("/<group_name>/node/<node_name>/")
@is_user_logged_in()
@is_admin()
def get_group_details_by_node_name(group_name, node_name):
    groups = cesi.groups
    group = groups.get(group_name, None)
    if not group:
        return jsonify(status="error", message="Wrong group name"), 400

    if node_name not in group:
        return jsonify(status="error", message="Wrong node name for group name"), 400

    result = {}
    n = cesi.get_node(node_name)
    processes = n.get_processes_by_group_name(group_name)
    result[n.name] = []
    for p in processes:
        result[n.name].append(p.serialize())

    print(result)
    return jsonify(status="success", result=result)
