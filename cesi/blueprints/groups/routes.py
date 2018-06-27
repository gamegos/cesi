from flask import (
    Blueprint,
    jsonify,
)

from core import (
    Cesi
)
from decorators import (
    is_user_logged_in,
    is_admin
)
from util import (
    ActivityLog
)

groups = Blueprint('groups', __name__)
cesi = Cesi.getInstance()
activity = ActivityLog.getInstance()

@groups.route('/')
@is_user_logged_in()
@is_admin()
def get_groups():
    _groups = set()
    for node in cesi.nodes:
        if node.is_connected:
            for p in node.processes:
                _groups.add(p.group)
        else:
            print(f"{node.name} is not connected.")

    # Set is not JSON serializable.
    return jsonify(groups=list(_groups))

@groups.route('/<group_name>')
@is_user_logged_in()
@is_admin()
def get_group_details(group_name):
    return jsonify({})
    #return jsonify(get_group_details(cesi, group_name))