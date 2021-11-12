import openstack
from falcon import secure_filename
from flask import Blueprint, render_template, request
from flask_login import login_required

from application.createArchitecture.Create_instance import create_image
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
