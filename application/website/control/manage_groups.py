import openstack
#from falcon import secure_filename
from flask import Blueprint, render_template, request
from flask_login import login_required

from application.website.control import db
from .models import User_in_group
from .permissions import user_has_permission
from .request_to_database import show_groups_for_current_professor, get_group_with_users

conn = openstack.connect(cloud='openstack')

manage_groups = Blueprint('manage_groups', __name__)


@manage_groups.route('/manage-groups', defaults={"group_name": None})
@manage_groups.route('/manage-groups/<group_name>')
@login_required
def get_manage_groups_page(group_name):
    group_with_users = get_group_with_users(group_name)

    return render_template("manage-groups.html",
                           user_has_permission=user_has_permission,
                           groups_for_current_professor=show_groups_for_current_professor(),
                           group_with_users=group_with_users,
                           group_name=group_name
                           )


# @manage_groups.route('/remove-user', defaults={"group_name": None})
@manage_groups.route('/remove-user/<group_name>', methods=['POST'])
@login_required
def delete_user_from_group(group_name):
    if request.method == 'POST':
        id_user_to_delete = request.form.get('idButtonForDelete')
        print(id_user_to_delete)
        User_in_group.query.filter_by(user_id=int(id_user_to_delete)).delete()
        db.session.commit()

    return get_manage_groups_page(group_name)
