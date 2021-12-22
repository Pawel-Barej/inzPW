from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    name_group = db.Column(db.String(150))


class User_in_group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))


class Uploaded_vm_image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    format = db.Column(db.String(15))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    expiration_date = db.Column(db.Integer)
    description = db.Column(db.String(150))
    uploaded_vm_image_id = db.Column(db.Integer, db.ForeignKey('uploaded_vm_image.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    architecture_id = db.Column(db.Integer, db.ForeignKey('architecture_for_assignment.id'))


class Users_assigned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))


class Architecture_for_assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    network_name = db.Column(db.String(150))
    subnet_name = db.Column(db.String(150))
    cidr = db.Column(db.String(150))
    gateway_ip = db.Column(db.String(150))
    router_name = db.Column(db.String(150))
    port_name = db.Column(db.String(150))


class General_settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Active_instance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    expiration_time = db.Column(db.String(150))
    address_ip = db.Column(db.String(150))
    booking_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
