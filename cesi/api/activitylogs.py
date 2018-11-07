from flask import Blueprint, jsonify

from core import Cesi
from decorators import is_user_logged_in
from loggers import ActivityLog

activitylogs = Blueprint("activitylogs", __name__)
cesi = Cesi.getInstance()
activity = ActivityLog.getInstance()


@activitylogs.route("/", methods=["GET"])
@is_user_logged_in()
def get_activity_log():
    try:
        with open(cesi.activity_log) as f:
            data = f.readlines()
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    return jsonify(status="success", logs=data[::-1])


@activitylogs.route("/<int:limit>/")
@is_user_logged_in()
def get_activity_log_with_limit(limit):
    try:
        with open(cesi.activity_log) as f:
            data = f.readlines()
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    return jsonify(status="success", logs=data[-limit::][::-1])


@activitylogs.route("/", methods=["DELETE"])
@is_user_logged_in()
def clear_activity_log():
    try:
        open(cesi.activity_log, "w").close()
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

    return jsonify(status="success")
