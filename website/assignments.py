from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from .permissions import user_has_permission

assignments = Blueprint('assignments', __name__)


@assignments.route('/your-assignments')
@login_required
def get_assignments_page():

    return render_template("assignments.html",
                           user_has_permission=user_has_permission
                           )