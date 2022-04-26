import threading
from datetime import timedelta, datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import time
import openstack

from application.infrastructure.Create_instance import delete_server
from application.infrastructure.Create_network import delete_network
from application.infrastructure.Create_router import delete_router, remove_interface_from_router


conn = openstack.connect(cloud='openstack')
db = SQLAlchemy()

from application.website.control.request_to_database import delete_instance, delete_assignment_and_architecture

DB_NAME = "database.db"
UPLOAD_FOLDER = 'static'


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)  # Auto wylogowanie po 5 minutach
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .manage_groups import manage_groups
    from .do_assignments import assignments
    from .create_assignments import create_assignments

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(manage_groups, url_prefix='/')
    app.register_blueprint(assignments, url_prefix='/')
    app.register_blueprint(create_assignments, url_prefix='/')


    from .models import User
    create_database(app)

    with app.app_context():
        threading.Thread(target=timer_for_elements,
                         args=(
                             app,)).start()


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def create_database(app):
    if not path.exists('application/website/control/' + DB_NAME):
        db.create_all(app=app)
        print('New Database!')


def timer_for_elements(app):
    from application.website.control.models import Active_instance, Assignment, Architecture_for_assignment

    while True:
        with app.app_context():
            get_expiration_date_instances = db.session.query(Active_instance.id, Active_instance.expiration_time, Active_instance.name).all()
            get_expiration_date_assignments = db.session.query(Assignment.name, Assignment.expiration_date).all()

        for date in get_expiration_date_instances:
            deadline = datetime.strptime(date[1], "%Y-%m-%dT%H:%M")
            actual_date = datetime.now()
            if deadline < actual_date:
                with app.app_context():
                    delete_server(conn, date[2])
                    delete_instance(date[0])

        for date in get_expiration_date_assignments:
            deadline = datetime.strptime(date[1], "%Y-%m-%dT%H:%M")
            actual_date = datetime.now()
            if deadline < actual_date:
                with app.app_context():
                    architecture_date = db.session.query(Architecture_for_assignment.router_name,
                                                         Architecture_for_assignment.network_name,
                                                         Architecture_for_assignment.subnet_name,
                                                         Architecture_for_assignment.port_name).filter(
                        Assignment.name == date[0],
                        Assignment.architecture_id == Architecture_for_assignment.id).first()
                    remove_interface_from_router(conn, architecture_date[0], architecture_date[2], architecture_date[3])
                    delete_router(conn, architecture_date[0])
                    delete_network(conn, architecture_date[1], architecture_date[2])
                    delete_assignment_and_architecture(date[0])



        time.sleep(10)
