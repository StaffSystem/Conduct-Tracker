from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user
from datetime import datetime, timedelta
from App.models import Staff
from App.database import db

from.index import index_views
from App.controllers import staff

from App.controllers import (
    create_user,
    jwt_authenticate,
    get_staff_email,
    login 
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_views.route('/signup',methods=['POST'])
def createStaff():
    try:
        data = request.get_json()

        # Check if email is already in use
        existing_staff = get_staff_email(data["email"])

        if existing_staff:
            return jsonify({"message": "Email is already in use"}), 401
        else:
            # Create a new Staff user
            user = Staff(staffID=data["staffId"], firstname=data["firstname"], lastname=data["lastname"], password=data["password"], email=data["email"], teachingExperience=data["te"])

            # Add the new user to the database and commit changes
            db.session.add(user)
            db.session.commit()

            return jsonify({"message": "Account Created"}), 201

    except Exception as e:
        # Log the error or return a meaningful error message
        print(f"Error creating staff account: {e}")
        db.session.rollback()
        return jsonify({"message": "Error creating staff account"}), 500

        
@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.get_json()
    user = login(data['email'], data['password'])
    
    if user:
        session['logged_in'] = True
        access_token = jwt_authenticate(data['email'], data['password'])
        return 'Account Logged in'
    return 'bad email or password given', 401


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    logout_user()
    return redirect('/'), jsonify('logged out!')