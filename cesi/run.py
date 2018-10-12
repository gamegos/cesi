#!/usr/bin/env python3
import argparse
import signal
import os

from flask import Flask, render_template, jsonify, g

from core import Cesi
from loggers import ActivityLog

__version__ = "2.4"

API_VERSION = "v2"


def configure(config_file_path):
    cesi = Cesi(config_file_path=config_file_path)
    activity = ActivityLog(log_path=cesi.activity_log)

    app = Flask(
        __name__,
        static_folder="ui/build",
        static_url_path="",
        template_folder="ui/build",
    )
    app.config.from_object(__name__)
    app.secret_key = os.urandom(24)

    app.add_url_rule("/", "index", lambda: render_template("index.html"))

    @app.before_request
    def _():
        # Open db connection
        g.db_conn = cesi.get_db_connection()

    app.teardown_appcontext(lambda _: g.db_conn.close())

    @app.errorhandler(404)
    def _(error):
        return jsonify(status="error", message=error.name), 404

    @app.errorhandler(400)
    def _(error):
        return jsonify(status="error", message=error.description), 400

    # or dynamic import
    from blueprints.nodes.routes import nodes
    from blueprints.activitylogs.routes import activitylogs
    from blueprints.environments.routes import environments
    from blueprints.groups.routes import groups
    from blueprints.users.routes import users
    from blueprints.auth.routes import auth
    from blueprints.profile.routes import profile

    app.register_blueprint(nodes, url_prefix="/{}/nodes".format(API_VERSION))
    app.register_blueprint(
        activitylogs, url_prefix="/{}/activitylogs".format(API_VERSION)
    )
    app.register_blueprint(
        environments, url_prefix="/{}/environments".format(API_VERSION)
    )
    app.register_blueprint(groups, url_prefix="/{}/groups".format(API_VERSION))
    app.register_blueprint(users, url_prefix="/{}/users".format(API_VERSION))
    app.register_blueprint(auth, url_prefix="/{}/auth".format(API_VERSION))
    app.register_blueprint(profile, url_prefix="/{}/profile".format(API_VERSION))

    signal.signal(signal.SIGHUP, lambda signum, frame: cesi.reload())

    return app, cesi


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cesi web server")

    parser.add_argument("-c", "--config-file", help="config file", required=True)
    parser.add_argument("--host", help="Host of the cesi", default="0.0.0.0")
    parser.add_argument("-p", "--port", help="Port of the cesi", default="5000")
    parser.add_argument(
        "--debug", help="Actived debug mode of the cesi", action="store_true"
    )
    parser.add_argument(
        "--auto-reload",
        help="Reload if app code changes (dev mode)",
        action="store_true",
    )
    parser.add_argument("--version", action="version", version=__version__)

    args = parser.parse_args()
    app, cesi = configure(args.config_file)

    app.run(
        host=args.host, port=args.port, use_reloader=args.auto_reload, debug=args.debug
    )
