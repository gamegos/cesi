from run import db
from models import User


def get_users():
    users = User.query.all()
    result = [{"name": user.username, "type": str(user.usertype)} for user in users]
    return result


def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return {}

    result = {"name": user.username, "type": user.usertype}
    return result


def delete_user(username):
    user = user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()


def add_user(username, password, usertype):
    User.register(username=username, password=password, usertype=usertype)


def validate_user(username, password):
    return User.verify(username, password)


def update_user_password(username, new_password):
    user = User.query.filter_by(username=username).first()
    user.set_password(new_password)
    db.session.commit()
