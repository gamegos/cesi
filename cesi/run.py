#!/usr/bin/env python3
import argparse
import signal
import os

from flask import Flask

from core import Cesi
from loggers import ActivityLog

VERSION = "v2"

app = Flask(__name__, static_folder='ui/build', static_url_path='', template_folder='ui/build')
app.config.from_object(__name__)
app.secret_key = os.urandom(24)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cesi web server')

    parser.add_argument(
        '-c', '--config',
        type=str,
        help='config file',
        required=True
    )

    args = parser.parse_args()
    cesi = Cesi(config_file_path=args.config)
    activity = ActivityLog(log_path=cesi.activity_log)

    from routes import *

    # or dynamic import
    from blueprints.nodes.routes import nodes
    from blueprints.activitylogs.routes import activitylogs
    from blueprints.environments.routes import environments
    from blueprints.groups.routes import groups
    from blueprints.users.routes import users
    app.register_blueprint(nodes, url_prefix="/{}/nodes".format(VERSION))
    app.register_blueprint(activitylogs, url_prefix="/{}/activitylogs".format(VERSION))
    app.register_blueprint(environments, url_prefix="/{}/environments".format(VERSION))
    app.register_blueprint(groups, url_prefix="/{}/groups".format(VERSION))
    app.register_blueprint(users, url_prefix="/{}/users".format(VERSION))

    signal.signal(signal.SIGHUP, lambda signum, frame: cesi.reload())

    app.run(
        host=cesi.host,
        port=cesi.port,
        use_reloader=cesi.auto_reload,
        debug=cesi.debug,
    )
