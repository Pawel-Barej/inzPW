import threading
from datetime import timedelta, datetime
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import time

db = SQLAlchemy()

from website.request_to_database import delete_instance

DB_NAME = "database.db"
UPLOAD_FOLDER = 'static'


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)  # Auto wylogowanie po 5 minutach
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .manage_groups import manage_groups
    from .do_assignments import assignments
    from .create_assignments import create_assignments

    from website.request_to_database import get_expiration_date_instance
    from website.request_to_database import get_expiration_date_architecture

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(manage_groups, url_prefix='/')
    app.register_blueprint(assignments, url_prefix='/')
    app.register_blueprint(create_assignments, url_prefix='/')

    from .models import User, Group, User_in_group, Uploaded_vm_image, Assignment, Users_assigned, \
        Architecture_for_assignment, General_settings, Active_instance

    with app.app_context():
        threading.Thread(target=timer_for_elements,
                         args=(get_expiration_date_architecture(),
                               app)).start()

    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


def timer_for_elements(get_expiration_date_assignments, app):
    from website.models import Active_instance
    with app.app_context():
        get_expiration_date_instances = db.session.query(Active_instance.id, Active_instance.expiration_time).all()

    while True:
        for date in get_expiration_date_assignments:
            deadline = datetime.strptime(date[1], "%Y-%m-%dT%H:%M")
            actual_date = datetime.now()
            if deadline < actual_date:
                print("This should be removed: " + date[0])

        for date in get_expiration_date_instances:
            deadline = datetime.strptime(date[1], "%Y-%m-%dT%H:%M")
            actual_date = datetime.now()
            if deadline < actual_date:
                with app.app_context():
                    print(date[1])
                    delete_instance(date[0])
                    print("i delete instance")

        with app.app_context():
            get_expiration_date_instances = db.session.query(Active_instance.id, Active_instance.expiration_time).all()

        time.sleep(10)
