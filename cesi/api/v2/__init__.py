import importlib

from flask import Blueprint, jsonify

API_VERSION = "v2"
API_PREFIX = "/api/{}".format(API_VERSION)


def register_blueprints(app,prefix=''):
    # Import and register blueprint modules dynamically
    #   from blueprints.nodes.routes import nodes
    #   app.register_blueprint(nodes, url_prefix="/{}/nodes".format(API_VERSION))
    blueprint_names = [
        "nodes",
        "activitylogs",
        "environments",
        "groups",
        "users",
        "auth",
        "profile",
    ]
    for blueprint_name in blueprint_names:
        module = importlib.import_module(
            "api.{}.{}".format(API_VERSION, blueprint_name)
        )
        blueprint = getattr(module, blueprint_name)
        app.register_blueprint(
            blueprint,
            url_prefix="{}/{}/{}".format(prefix, API_PREFIX, blueprint_name)
        )
