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
    identifier = db.Column(db.String(50))
    name = db.Column(db.String(50))
    description = db.Column(db.String(150))
    expiration_date = db.Column(db.Integer)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(150))
    uploaded_vm_image_id = db.Column(db.Integer)
    creator_id = db.Column(db.Integer)

class Users_assigned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))