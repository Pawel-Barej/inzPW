from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import openstack
from flask_login import  login_required

from application.createArchitecture.Create_instance import create_image
from .permissions import user_has_permission

conn = openstack.connect(cloud='openstack')
create_assignments = Blueprint('create_assignments', __name__)

@create_assignments.route('/create-assignments',methods=['GET','POST'])
@login_required
def get_create_assignments_page():

    if request.method == 'POST':
        files = request.files.get('file')
        print(files)
        #create_image(conn, files)

    return render_template("create-assignments.html",
                           user_has_permission=user_has_permission
                           )