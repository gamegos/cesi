from run import db
from models import User
from utils import convert_user_object_to_dict


def get_users():
    users = User.query.all()
    result = [convert_user_object_to_dict(user) for user in users]
    return result


def get_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    result = convert_user_object_to_dict(user)
    return result


def check_database():
    try:
        ### Create Tables
        db.create_all()
        ### Add Admin User
        admin_user = User.register(username="admin", password="admin", usertype=0)
    except Exception as e:
        print(e)
