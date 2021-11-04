from flask import Blueprint, render_template, flash, redirect, url_for, Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Group, User, UserInGroup
from . import db
from .permissions import user_has_permission
from .request_to_database import show_users, show_groups, show_groups_for_current_professor

views = Blueprint('views', __name__)


@views.route('/main', methods=['GET'])
@login_required
def get_main_page():
    return render_template("home.html",
                           current_user=current_user,
                           users=show_users(),
                           groups=show_groups(),
                           groups_for_current_professor=show_groups_for_current_professor(),
                           user_has_permission=user_has_permission,
                           )


@views.route('/create-group', methods=['POST'])
@login_required
def create_group():
    if user_has_permission("table_users"):
        if request.method == 'POST':

            group = request.form.get('nameForGroup')
            wrong_name_group = Group.query.filter_by(name_group=group).first()

            if wrong_name_group:
                flash('This group already exists.', category='error')  # Sprawdzić dlaczego nie działa
            elif len(group) < 3:
                flash('Name is too short', category='error')
            else:
                new_group = Group(name_group=group, id_owner=current_user.id)
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
        id_button_for_user = request.form.get('idButtonForUser')

        user = User.query.filter_by(id=int(id_button_for_user)).first()
        user.role = role
        db.session.commit()

    return get_main_page()


@views.route('/add-user-to-group', methods=['POST'])
@login_required
def add_user_to_group():
    if request.method == 'POST':
        group = request.form.get('check')
        id_button_for_user = request.form.get('idButtonForUser')
        list_of_groups = group.split(',')
        list_of_groups = list(filter(None, list_of_groups))

        for group in list_of_groups:
            group_for_id = Group.query.filter_by(name_group=group).first()
            group = group_for_id.id
            if db.session.query(UserInGroup).filter(UserInGroup.user_id.like(id_button_for_user),
                                                    UserInGroup.group_id.like(group)).first() != None:
                flash('This user already is in:', category='error')
            else:
                connect_user_with_groups = UserInGroup(user_id=id_button_for_user, group_id=group_for_id.id)
                db.session.add(connect_user_with_groups)
                db.session.commit()

    return get_main_page()
