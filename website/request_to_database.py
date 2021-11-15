from flask_login import current_user
from .models import Group, User, User_in_group, Uploaded_vm_image, Users_assigned, Assignment, \
    Architecture_for_assignment
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
    result = db.session.query(User.email, User.first_name).select_from(Group).join(User_in_group).join(
        User).filter(
        Group.id_owner == current_user.id, Group.name_group == name_group).all()

    return result

def get_your_image():

    result = filter(lambda upload_vm_image: upload_vm_image.creator_id == current_user.id,
                    db.session.query(Uploaded_vm_image).all())

    return result

def get_users_in_group(id_group):
    result = db.session.query(User_in_group.user_id).filter(User_in_group.group_id == id_group).all()

    return result

def get_assignment(assignemnt_name):
    result = db.session.query(Assignment.id).filter(Assignment.name == assignemnt_name)

    return result

def get_architecture_for_assignment():
    result = db.session.query(Architecture_for_assignment.network_name).all()

    return result