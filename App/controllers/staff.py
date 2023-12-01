from App.controllers.user import get_staff
from App.models import Staff, Student, Review, Karma
from App.database import db

def create_review(staffID, studentID, is_positive, comment):
    staff = get_staff(staffID)
    student = db.session.query(Student).get(studentID)
    
    if staff and student:
        review = staff.createReview(student,is_positive, comment)
        return review
    return None

def get_staff_reviews(staff_id):
    staff = get_staff(staff_id)
    if staff:
        return staff.getReviewsByStaff(staff)


def create_student(studentID, firstname, lastname, contact, studentType, program):
    new_student = Student(studentID, firstname=firstname, lastname=lastname, contact=contact, studentType=studentType, program=program)
    if new_student:
        return new_student
    return None

def search_students_searchTerm(staff, searchTerm):
    students = staff.searchStudent(searchTerm)
    if students:
      return students
    return None

def create_staff(firstname, lastname, password, staffID, email, teachingExperience):
    new_staff = Staff.addStaff(self = Staff, id=staffID, firstname=firstname, lastname=lastname, password=password, email=email, teachingExperience=teachingExperience)
    
    if new_staff:
	        return new_staff
    else:
	    return None
  