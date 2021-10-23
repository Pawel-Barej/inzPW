from flask import Blueprint, render_template, flash, redirect, url_for, Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Group, User
from . import db
from .permissions import user_has_permission
from .request_to_database import show_users, show_groups

views = Blueprint('views', __name__)

@views.route('/main', methods=['GET'])
@login_required
def get_main_page():

    return render_template("home-Admin.html",
                           current_user=current_user,
                           users=show_users(),
                           groups=show_groups(),
                           user_has_permission=user_has_permission)

@views.route('/create-group', methods=['POST'])
@login_required
def create_group():
    if request.method == 'POST':

        group = request.form.get('name')
        wrong_name_group = Group.query.filter_by(name_group=group).first()

        if wrong_name_group:
            flash('This group already exists.', category='error')
        elif len(group) < 3:
            flash('Name is too short', category='error')
        else:
            new_group = Group(name_group=group)
            db.session.add(new_group)
            db.session.commit()
            flash('New group added', category='success')

        # if request.form.get('action1') == 'create instance':
        #     init(conn)
        # if request.form.get('action2') == 'delete instance':
        #     delete_architecture(conn)
        return get_main_page()

@views.route('/change-role', methods=['POST'])
@login_required
def change_role():
    if request.method == 'POST':
        role = request.form.get('role')
        id_button = request.form.get('idButton')
        user = User.query.filter_by(id=int(id_button)).first()
        user.role=role
        db.session.commit()

    return get_main_page()



