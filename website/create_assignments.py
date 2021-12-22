from flask import Blueprint, render_template, request
import openstack
from flask_login import login_required, current_user

from application.createArchitecture.Create_network import create_network_with_subnets, create_port
from application.createArchitecture.Create_router import create_router, add_interface_to_router
from . import db
from application.createArchitecture.Create_instance import create_image, delete_image
from .models import Uploaded_vm_image, Assignment, Users_assigned, Architecture_for_assignment
from .permissions import user_has_permission
from .request_to_database import get_your_image, show_groups_for_current_professor, get_group_with_users, \
    get_users_in_group, get_assignment, get_architecture_for_assignment, get_assignment_cuurent_professor

conn = openstack.connect(cloud='openstack')
create_assignments = Blueprint('create_assignments', __name__)


@create_assignments.route('/create-assignments', methods=['GET', 'POST'])
@login_required
def get_create_assignments_page():
    return render_template("create-assignments.html",
                           user_has_permission=user_has_permission,
                           images=get_your_image(),
                           groups=show_groups_for_current_professor(),
                           images_for_modal=get_your_image(),
                           created_assignments=get_assignment_cuurent_professor()
                           )


@create_assignments.route('/upload-image', methods=['GET', 'POST'])
@login_required
def upload_image():
    if request.method == 'POST':
        file_with_image = request.files.get('file')
        image_name = request.form.get('image-name')
        disk_format = request.form.get('image-format')
        create_image(conn, image_name, file_with_image, disk_format)

        new_image = Uploaded_vm_image(name=image_name, format=disk_format, creator_id=current_user.id)
        db.session.add(new_image)
        db.session.commit()

    return get_create_assignments_page()


@create_assignments.route('/delete_image', methods=['GET', 'POST'])
@login_required
def delete_image_from_list():
    if request.method == 'POST':
        id_image_to_delete = request.form.get('idButtonForImage')
        print(id_image_to_delete)
        name_image = db.session.query(Uploaded_vm_image).filter(Uploaded_vm_image.id == id_image_to_delete).first()

        delete_image(conn, name_image.name)
        db.session.query(Uploaded_vm_image).filter_by(id=id_image_to_delete).delete()
        db.session.commit()

    return get_create_assignments_page()


@create_assignments.route('/create_architecture', methods=['GET', 'POST'])
@login_required
def create_architecture():
    if request.method == 'POST':
        assignment_name = request.form.get('assignmentName')
        assignment_description = request.form.get('assignmentDescription')
        id_group_for_architecture = request.form.get('idGroupForArchitecture')
        id_image_for_architecture = request.form.get('idImageForArchitecture')
        assignment_datatime_end = request.form.get('assignmentDatatimeEnd')

        table = []
        i = 1
        for network in get_architecture_for_assignment():
            table.append(network[0])

        new_network_name = "remote_eye_network-"
        while True:
            if new_network_name + str(i) in table:
                i = i + 1
            else:
                new_network_name = new_network_name + str(i)
                break

        new_cidr = '192.168.' + str(10 + int(new_network_name.split("-")[1])) + '.0/24'
        new_gateway_ip = '192.168.' + str(10 + int(new_network_name.split("-")[1])) + '.1'
        new_subnet_name = "remote_eye_subnet-" + new_network_name.split("-")[1]
        new_router_name = "remote_eye_router-" + new_network_name.split("-")[1]
        new_port_name = "remote_eye_port-" + new_network_name.split("-")[1]

        new_architecture = Architecture_for_assignment(network_name=new_network_name,
                                                       subnet_name=new_subnet_name,
                                                       cidr=new_cidr,
                                                       gateway_ip=new_gateway_ip,
                                                       router_name=new_router_name,
                                                       port_name=new_port_name)

        db.session.add(new_architecture)
        db.session.commit()

        new_assignment = Assignment(name=assignment_name,
                                    expiration_date=assignment_datatime_end,
                                    description=assignment_description,
                                    uploaded_vm_image_id=id_image_for_architecture,
                                    creator_id=current_user.id,
                                    architecture_id=db.session.query(Architecture_for_assignment.id).order_by(
                                        Architecture_for_assignment.id.desc()).first().id)
        db.session.add(new_assignment)
        db.session.commit()

        for user_id in get_users_in_group(id_group_for_architecture):
            id = int(str(user_id).replace("(", "").replace(")", "").replace(",", ""))
            users_assigned = Users_assigned(user_id=id,
                                            assignment_id=get_assignment(assignment_name))
            db.session.add(users_assigned)
            db.session.commit()

        create_network_with_subnets(conn, new_network_name, new_subnet_name, new_cidr, new_gateway_ip)
        create_port(conn, new_port_name, new_network_name)
        create_router(conn, new_router_name)
        add_interface_to_router(conn, new_router_name, new_subnet_name, new_port_name)

    return get_create_assignments_page()
