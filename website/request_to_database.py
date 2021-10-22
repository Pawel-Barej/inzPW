from .models import Group, User
from . import db

def show_users():
    results = db.session.query(User).all()

    return results

def show_groups():
    results = db.session.query(Group).all()

    return results