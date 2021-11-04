from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from .permissions import user_has_permission
from .request_to_database import show_groups_for_current_professor, get_group_with_users

manage_groups = Blueprint('manage_groups', __name__)


@manage_groups.route('/manage-groups')
@login_required
def get_manage_groups_page():
    return render_template("manage-groups.html",
                           user_has_permission=user_has_permission,
                           groups_for_current_professor=show_groups_for_current_professor()
                           )


@manage_groups.route('/manage-groups/refresh-table', methods=['PUT'])
@login_required
def refresh_table():
    group_name = request.form.get('nameGroup')
    group_with_users = get_group_with_users(group_name)

    return render_template("manage-groups.html",
                           user_has_permission=user_has_permission,
                           groups_for_current_professor=show_groups_for_current_professor(),
                           group_with_users=group_with_users,
                           group_name=group_name
                           )
