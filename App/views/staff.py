
import random
import string
from flask import Blueprint, request, jsonify
from App.controllers import Student, Staff
from App.controllers.user import get_staff, get_student
from App.database import db
from flask_jwt_extended import current_user as jwt_current_user
from flask_jwt_extended import jwt_required
from App.controllers import staff

from App.controllers.staff import (
    search_students_searchTerm, 
    create_review
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')


@staff_views.route('/signup',methods=["POST"])
def createStaff():
    data = request.get_json()
    taken_name=staff.get_staff_email(data["email"])

    if(taken_name):
        return jsonify({"email": "email already in use"}),401
    else: 
        user = staff.create_staff(data["staffId"], data["email"], data["firstname"], data["lastname"], data["password"], data["te"])
    if(user):
        return jsonify({"message": "Account Created"}),201
    

@staff_views.route('/staff/<string:staff_id>', methods=['GET'])
def get_staff_action(staff_id):
    staff = get_staff(str(staff_id))
    if staff:
        return jsonify(staff.to_json())
    return 'Staff not found', 404

@staff_views.route('/student/<string:student_id>/reviews', methods=['POST'])
# @jwt_required()
def create_review_action(student_id):
    # if not jwt_current_user or not isinstance(jwt_current_user, Staff):#check if user is authorized
    #   return 'Unauthorized', 401

    student= get_student(str(student_id))#get the student 

    if not student:
        return jsonify({"error": 'Student does not exist'}), 404

    data = request.json
    if not data['comment']:
        return "Invalid request data", 400
    
    if data['isPositive'] not in (True, False):
        return jsonify({"message": f"invalid Positivity ({data['isPositive']}). Positive: true or false"}), 400

    # if not get_staff(str(jwt_current_user.ID)):
    #     return 'Staff does not exist', 404 

    review = create_review(data['staffId'], student_id, data['isPositive'], data['comment'])
    
    if review:
        return jsonify(review.to_json()), 201
    return 'Failed to create review', 400

