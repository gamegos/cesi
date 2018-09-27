from flask import Blueprint, jsonify

from core import Cesi
from decorators import is_user_logged_in

environments = Blueprint("environments", __name__)
cesi = Cesi.getInstance()


@environments.route("/")
@is_user_logged_in()
def get_environments():
    return jsonify(status="success", environments=cesi.serialize_environments())


@environments.route("/<env_name>/")
@is_user_logged_in()
def get_environment_details(env_name):
    _environment = cesi.get_environment_or_400(env_name)
    return jsonify(status="success", environment=_environment.serialize())
