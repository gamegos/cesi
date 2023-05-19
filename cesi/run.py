#!/usr/bin/env python3
import argparse
import signal
import os
import importlib

from flask import Flask, render_template, jsonify, g
from flask_sqlalchemy import SQLAlchemy

from version import __version__

db = SQLAlchemy()


def create_app(cesi):
    from api.v2 import register_blueprints

    app = Flask(
        __name__,
        static_folder="ui/build",
        static_url_path="",
        template_folder="ui/build",
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = cesi.database
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.urandom(24)

    db.init_app(app)

    app.add_url_rule("/", "index", lambda: render_template("index.html"))
    app.add_url_rule(
        "/api/version",
        "version",
        lambda: jsonify(status="success", version=__version__),
    )

    @app.errorhandler(404)
    @app.errorhandler(400)
    def _(error):
        return jsonify(status="error", message=error.description), error.code

    register_blueprints(app)

    return app


def configure(config_file_path):
    from core import Cesi
    from loggers import ActivityLog
    from controllers import check_database

    cesi = Cesi(config_file_path=config_file_path)
    _ = ActivityLog(log_path=cesi.activity_log)

    app = create_app(cesi)

    # Check database
    with app.app_context():
        check_database()

    signal.signal(signal.SIGHUP, lambda signum, frame: cesi.reload())



    return app, cesi

class PrefixMiddleware(object):
    '''
    source: https://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes/36033627#36033627
    '''
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix
    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cesi web server")

    parser.add_argument(
        "-c", "--config-file", "--config", help="config file", required=True
    )
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
    parser.add_argument(
        "--url_prefix",
        default = '',
    )

    args = parser.parse_args()
    app, cesi = configure(args.config_file)

    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=args.url_prefix)

    app.run(
        host=args.host, port=args.port, use_reloader=args.auto_reload, debug=args.debug
    )
