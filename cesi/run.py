#!/usr/bin/env python3
import argparse
import signal
import os

from flask import Flask, render_template, jsonify, g

from core import Cesi
from loggers import ActivityLog

VERSION = "v2"


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

    app.register_blueprint(nodes, url_prefix="/{}/nodes".format(VERSION))
    app.register_blueprint(activitylogs, url_prefix="/{}/activitylogs".format(VERSION))
    app.register_blueprint(environments, url_prefix="/{}/environments".format(VERSION))
    app.register_blueprint(groups, url_prefix="/{}/groups".format(VERSION))
    app.register_blueprint(users, url_prefix="/{}/users".format(VERSION))
    app.register_blueprint(auth, url_prefix="/{}/auth".format(VERSION))
    app.register_blueprint(profile, url_prefix="/{}/profile".format(VERSION))

    signal.signal(signal.SIGHUP, lambda signum, frame: cesi.reload())

    return app, cesi


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cesi web server")

    parser.add_argument("-c", "--config", type=str, help="config file", required=True)

    args = parser.parse_args()

    app, cesi = configure(args.config)

    app.run(
        host=cesi.host, port=cesi.port, use_reloader=cesi.auto_reload, debug=cesi.debug
    )
