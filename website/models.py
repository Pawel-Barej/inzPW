from . import db
from flask_login import UserMixin

class UserInGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    name_group = db.Column(db.String(150))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String)


