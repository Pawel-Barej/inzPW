from flask_login import current_user
from .models import Group, User, UserInGroup
from . import db


def show_users():
    results = db.session.query(User).all()

    return results


def show_groups():
    results = db.session.query(Group).all()

    return results


def show_groups_for_current_professor():
    results = filter(lambda group: group.id_owner == current_user.id, db.session.query(Group).all())

    return results


def get_group_with_users(name_group):
    result = db.session.query(User.email, User.first_name).select_from(Group).join(UserInGroup).join(
        User).filter(
        Group.id_owner == current_user.id, Group.name_group == name_group).all()

    return result
