from flask import Blueprint, render_template
from flask import Flask, Blueprint, render_template, request
from flask_login import login_required, current_user
from application.createArchitecture.init import *
from application.createArchitecture.delete_architecture import *
from threading import Timer

views = Blueprint('views', __name__)

@views.route('/main', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if request.form.get('action1') == 'create instance':
            init(conn)
        elif request.form.get('action2') == 'delete instance':
            delete_architecture(conn)

    elif request.method == 'GET':
        return render_template('home-Admin.html', user=current_user)

    return render_template("home-Admin.html", user=current_user)


