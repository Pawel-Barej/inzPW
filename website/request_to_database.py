from flask_login import current_user
from .models import Group, User, User_in_group, Uploaded_vm_image, Users_assigned, Assignment, \
    Architecture_for_assignment, Active_instance
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


def get_assignment(assignment_name):
    result = db.session.query(Assignment.id).filter(Assignment.name == assignment_name)

    return result


def get_architecture_for_assignment():
    result = db.session.query(Architecture_for_assignment.network_name).all()

    return result


def get_assignment_cuurent_professor():
    result = filter(lambda assignment: assignment.creator_id == current_user.id, db.session.query(Assignment).all())
    return result


def get_assignment_curent_user():
    result = db.session.query(Assignment.name, Assignment.expiration_date,
                              Architecture_for_assignment.network_name).select_from(
        Assignment).join(Users_assigned).join(Uploaded_vm_image).join(Architecture_for_assignment).filter(
        Assignment.uploaded_vm_image_id == Uploaded_vm_image.id, Users_assigned.user_id == current_user.id,
        Assignment.architecture_id == Architecture_for_assignment.id).all()
    return result


def get_network_name_from_assignment(assignment_name):
    result = db.session.query(Assignment.id, Architecture_for_assignment.network_name,
                              Uploaded_vm_image.name).select_from(
        Assignment).join(Architecture_for_assignment).join(Uploaded_vm_image).filter(
        Assignment.name == assignment_name, Assignment.uploaded_vm_image_id == Uploaded_vm_image.id,
        Assignment.architecture_id == Architecture_for_assignment.id).first()

    return result


def get_expiration_date_architecture():
    result = db.session.query(Assignment.name, Assignment.expiration_date).all()

    return result


def get_expiration_date_instance():
    result = db.session.query(Active_instance.id, Active_instance.expiration_time).all()

    return result


def delete_instance(instance_id):
    Active_instance.query.filter(Active_instance.id == instance_id).delete()
    db.session.commit()


def delete_assignment_and_architecture(assignment_name):
    id_assignment = db.session.query(Assignment.id).filter(Assignment.name == assignment_name).first()

    result = db.session.query(Assignment.architecture_id).filter(Assignment.name == assignment_name).first()

    Users_assigned.query.filter(Users_assigned.assignment_id == id_assignment[0]).delete()
    Architecture_for_assignment.query.filter(Architecture_for_assignment.id == result[0]).delete()
    Assignment.query.filter(Assignment.name == assignment_name).delete()
    db.session.commit()


def get_time_max(assignment_id):
    result = db.session.query(Assignment.expiration_date).filter(Assignment.id == assignment_id).first()

    return result


def get_user_instance():
    result = db.session.query(Active_instance.expiration_time, Active_instance.address_ip).filter(
        Active_instance.booking_user_id == current_user.id)

    return result
