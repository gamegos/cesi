from flask import (
    Blueprint,
    jsonify,
)

from core import Cesi
from decorators import is_user_logged_in
from loggers import ActivityLog

activitylogs = Blueprint('activitylogs', __name__)
cesi = Cesi.getInstance()
activity = ActivityLog.getInstance()

@activitylogs.route('/')
@is_user_logged_in()
def get_activity_log():
    try:
        with open(cesi.activity_log) as f:
            data = f.readlines()
    except Exception as e:
            return jsonify(status="error", message=str(e))

    return jsonify(status="success", log=data)

@activitylogs.route('/<int:limit>/')
@is_user_logged_in()
def get_activity_log_with_limit(limit):
    try:
        with open(cesi.activity_log) as f:
            data = f.readlines()
    except Exception as e:
            return jsonify(status="error", message=str(e))

    return jsonify(status="success", log=data[-limit:])