from flask import Blueprint, render_template, request
import openstack
from flask_login import login_required, current_user
from . import db
from application.createArchitecture.Create_instance import create_image, delete_image
from .models import Uploaded_vm_image
from .permissions import user_has_permission
from .request_to_database import get_your_image

conn = openstack.connect(cloud='openstack')
create_assignments = Blueprint('create_assignments', __name__)

@create_assignments.route('/create-assignments',methods=['GET','POST'])
@login_required
def get_create_assignments_page():

    return render_template("create-assignments.html",
                           user_has_permission=user_has_permission,
                           images = get_your_image()
                           )

@create_assignments.route('/upload-image',methods=['GET','POST'])
@login_required
def upload_image():
    if request.method == 'POST':
        file_with_image = request.files.get('file')
        image_name = request.form.get('image-name')
        disk_format = request.form.get('image-format')
        create_image(conn,image_name, file_with_image, disk_format)

        new_image = Uploaded_vm_image(name=image_name, format=disk_format, creator_id=current_user.id)
        db.session.add(new_image)
        db.session.commit()

    return  get_create_assignments_page()

@create_assignments.route('/delete_image',methods=['GET','POST'])
@login_required
def delete_image_():
    if request.method == 'POST':
        id_image_to_delete = request.form.get('idButtonForImage')
        print(id_image_to_delete)
        name_image = db.session.query(Uploaded_vm_image).filter(Uploaded_vm_image.id == id_image_to_delete).first()

        delete_image(conn,name_image.name)
        db.session.query(Uploaded_vm_image).filter_by(id=id_image_to_delete).delete()
        db.session.commit()

        return get_create_assignments_page()