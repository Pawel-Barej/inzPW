from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, flash

from application.infrastructure.Create_instance import create_server, add_floating_ip_to_server, create_ip
from .models import Active_instance
from application.website.control import db
from flask_login import login_required, current_user

from .permissions import user_has_permission
from .request_to_database import get_assignment_curent_user, get_network_name_from_assignment, \
    get_time_max, get_user_instance, get_active_instance
import openstack

conn = openstack.connect(cloud='openstack')

assignments = Blueprint('assignments', __name__)


@assignments.route('/your-assignments')
@login_required
def get_assignments_page():
    return render_template("assignments.html",
                           user_has_permission=user_has_permission,
                           assignments=get_assignment_curent_user(),
                           instances=get_user_instance()
                           )


@assignments.route('/resource-reservation', methods=['POST'])
@login_required
def resource_reservation():
    reservation_time = request.form.get('reservationTime')
    name_assignment_for_user = request.form.get('idButtonForUser')

    reservation_end_time = datetime.now() + timedelta(hours=int(reservation_time))
    dt_string = reservation_end_time.strftime("%Y-%m-%d" + "T" + "%H:%M")

    index_network_name_image_name = get_network_name_from_assignment(name_assignment_for_user)

    deadline = datetime.strptime(get_time_max(index_network_name_image_name[0])[0], "%Y-%m-%dT%H:%M")

    if reservation_end_time >= deadline:
        reservation_end_time = deadline - timedelta(minutes=5)
        dt_string = reservation_end_time.strftime("%Y-%m-%d" + "T" + "%H:%M")

    def create_server_for_user():
        create_server(conn, index_network_name_image_name[2], index_network_name_image_name[1],
                      "instance_for: " + current_user.email + " " + name_assignment_for_user)

        address_ip = create_ip(conn)
        print(address_ip)

        add_floating_ip_to_server(conn, "instance_for: " + current_user.email + " " + name_assignment_for_user,
                                  address_ip)

        create_instance = Active_instance(expiration_time=dt_string,
                                          name="instance_for: " + current_user.email + " " + name_assignment_for_user,
                                          address_ip=address_ip,
                                          booking_user_id=current_user.id,
                                          assignment_id=index_network_name_image_name[0])
        db.session.add(create_instance)
        db.session.commit()

    print(get_active_instance())

    if get_active_instance() != []:
        for instance in get_active_instance()[0]:
            flash('This user already is in:', category='error')
            if instance != ("instance_for: " + current_user.email + " " + name_assignment_for_user):
                create_server_for_user()
    else:
        create_server_for_user()

    return get_assignments_page()
