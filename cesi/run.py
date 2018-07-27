#!/usr/bin/env python3
import argparse
import signal

from flask import Flask

from core import Cesi
from loggers import ActivityLog

VERSION = "v2"

app = Flask(__name__)
app.config.from_object(__name__)

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
    app.secret_key = cesi.secret_key
    
    from routes import *

    # or dynamic import
    from blueprints.nodes.routes import nodes
    from blueprints.activitylogs.routes import activitylogs
    from blueprints.environments.routes import environments
    from blueprints.groups.routes import groups
    from blueprints.users.routes import users
    app.register_blueprint(nodes, url_prefix=f"/{VERSION}/nodes")
    app.register_blueprint(activitylogs, url_prefix=f"/{VERSION}/activitylogs")
    app.register_blueprint(environments, url_prefix=f"/{VERSION}/environments")
    app.register_blueprint(groups, url_prefix=f"/{VERSION}/groups")
    app.register_blueprint(users, url_prefix=f"/{VERSION}/users")

    signal.signal(signal.SIGHUP, lambda signum, frame: cesi.reload())

    app.run(
        host=cesi.host,
        port=cesi.port,
        use_reloader=cesi.auto_reload,
        debug=cesi.debug,
    )
