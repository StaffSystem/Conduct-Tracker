
from flask.cli import AppGroup, FlaskGroup
from flask import Blueprint, request, jsonify
from App.controllers import Student, Staff
from App.controllers.user import get_staff, get_student
from App.controllers.staff import get_staff_email
from App.database import db
from flask_jwt_extended import current_user as jwt_current_user
from flask_jwt_extended import jwt_required
from App.controllers import student 

from App.controllers.staff import (
    search_students_searchTerm, 
    create_review
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')


# @staff_views.route('/signup',methods=["POST"])
# def createStaff():
#     data = request.get_json()
#     taken_name=get_staff_email(data["email"])

#     if(taken_name):
#         return jsonify({"email": "email already in use"}),401
#     else: 
#         user = staff.create_staff(data["staffID"], data["email"], data["firstname"], data["lastname"], data["password"], data["te"])
#     if(user):
#         return jsonify({"message": "Account Created"}),201
    

# @staff_views.route('/login',methods=["login"])
# def login_action():
#     data = request.get_json()
#     staff = Staff.query.filter_by(email=email).first()
#     if staff and staff.check_password(password):
#         access_token = create_access_token(identity = staff.ID)
#         return jsonify(access_token=access_token)
#     else:
#         return jsonify({"message": "Incorrect Username or Password"}),401


# @staff_views.route('/staff/<string:staff_id>', methods=['GET'])
# def get_staff_action(staff_id):
#     staff = get_staff(str(staff_id))
#     if staff:
#         return jsonify(staff.to_json())
#     return 'Staff not found', 404

@staff_views.route('/searchStudent',methods=["GET"])
# @login_required
def searchStudent():
    data=request.get_json()
    requested_student=student.get_student(data["id"])
    if(requested_student):
        print(requested_student.to_json())
        return jsonify({"message": "Student Found", **requested_student.to_json()}),201
    else:
        return jsonify({"message": "Invalid Student Id Given"}),400


@staff_views.route('/student/<string:student_id>/reviews', methods=['POST'])
# @jwt_required()
def create_review_action(student_id):
    # if not jwt_current_user or not isinstance(jwt_current_user, Staff):
    #   return 'Unauthorized', 401

    student= get_student(str(student_id))

    if not student:
        return jsonify({"error": 'Student does not exist'}), 404

    data = request.json
    if not data['comment']:
        return "Invalid request data", 400
    
    if data['isPositive'] not in (True, False):
        return jsonify({"message": f"invalid Positivity ({data['isPositive']}). Positive: true or false"}), 400

    review = create_review(data["staffID"], student_id, data['isPositive'], data['comment'])
    
    if review:
        return jsonify(review.to_json()), 201
    return 'Failed to create review', 400




    

# @staff_views.route('/students/search/<string:search_term>', methods=['GET'])
# @jwt_required()
# def search_students(search_term):
#   if jwt_current_user and isinstance(jwt_current_user, Staff): 
#     students = search_students_searchTerm(jwt_current_user, search_term)
#     if students:
#       return jsonify([student for student in students]), 200
#     else:
#       return jsonify({"message": f"No students found with search term {search_term}"}), 204
#   else:
#     return jsonify({"message": "You are not authorized to perform this action"}), 401
