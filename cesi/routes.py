from flask import (
    Flask,
    render_template,
    redirect,
    jsonify,
    request,
    g,
    session,
    url_for,
)

from core import Cesi
from loggers import ActivityLog
from decorators import is_user_logged_in, is_admin, is_admin_or_normal_user
from run import app, VERSION

cesi = Cesi.getInstance()
activity = ActivityLog.getInstance()

# Open database connection
@app.before_request
def before_request():
    g.db_conn = cesi.get_db_connection()


# Close database connection
@app.teardown_appcontext
def close_connection(_):
    g.db_conn.close()


@app.errorhandler(404)
def page_not_found(error):
    return jsonify(status="error", message="page not found")


@app.errorhandler(400)
def not_found(error):
    return jsonify(status="error", message=error.description)


@app.route("/{}/userinfo/".format(VERSION))
@is_user_logged_in()
def user_info():
    return jsonify(
        status="success",
        username=session["username"],
        usertypecode=session["usertypecode"],
    )


@app.route("/{}/initdb/".format(VERSION))
def initdb():
    cesi.drop_database()
    cesi.check_database()
    return jsonify(status="success", message="Yeah, We initialized the database.")


@app.route("/")
def showMain():
    return render_template("index.html")
