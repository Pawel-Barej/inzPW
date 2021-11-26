from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from application.createArchitecture.Create_instance import create_server
from .models import User, Active_instance
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from .permissions import user_has_permission
from .request_to_database import get_assignment_curent_user, get_assignment, get_network_name_from_assignment
import openstack

conn = openstack.connect(cloud='openstack')

assignments = Blueprint('assignments', __name__)


@assignments.route('/your-assignments')
@login_required
def get_assignments_page():
    return render_template("assignments.html",
                           user_has_permission=user_has_permission,
                           assignments=get_assignment_curent_user()
                           )


@assignments.route('/resource-reservation', methods=['POST'])
@login_required
def resource_reservation():
    reservation_time = request.form.get('reservationTime')
    name_assignment_for_user = request.form.get('idButtonForUser')

    now = datetime.now() + timedelta(hours=int(reservation_time))
    dt_string = now.strftime("%Y-%m-%d" + "T" + "%H:%M")

    index_network_name_image_name = get_network_name_from_assignment(name_assignment_for_user)

    create_server(conn, index_network_name_image_name[2], index_network_name_image_name[1],
                  "instance_for: " + current_user.email)

    create_instance = Active_instance(expiration_time=dt_string,
                                      booking_user_id=current_user.id,
                                      assignment_id=index_network_name_image_name[0])
    db.session.add(create_instance)
    db.session.commit()

    return get_assignments_page()
