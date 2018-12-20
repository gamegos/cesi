from flask import Blueprint, jsonify

from core import Cesi
from decorators import is_user_logged_in

environments = Blueprint("environments", __name__)
cesi = Cesi.getInstance()


@environments.route("/")
@is_user_logged_in()
def get_environments():
    return jsonify(status="success", environments=cesi.serialize_environments())
