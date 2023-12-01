from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user
from datetime import datetime, timedelta

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate,
    jwt_authenticate_admin,
    login 
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_views.route('/signup', methods=['POST'])
def login_action():
    data = request.json
    if user:
        session['logged_in'] = True
        token = jwt_authenticate(data['ID'], data['password'])
        return 'user logged in!'
    return 'bad username or password given', 401

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.json
    user = login(data['ID'], data['password'])
    if user:
        session['logged_in'] = True
        token = jwt_authenticate(data['ID'], data['password'])
        return 'user logged in!'
    return 'bad username or password given', 401


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    logout_user()
    return redirect('/'), jsonify('logged out!')