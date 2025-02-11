from App.controllers.user import get_staff
from App.models import Staff, Student, Review, Karma
from App.database import db


def create_review(staffID, studentID, is_positive, comment):
    staff = Staff.query.filter_by(staff_id=staffID).first()
    student = Student.query.filter_by(ID=studentID).first()

    if staff and student:
        review = staff.createReview(staff,student,is_positive, comment)
        return review
    return None




def get_staff_reviews(staff_id):
    staff = get_staff(staff_id)
    if staff:
        return staff.getReviewsByStaff(staff)


def get_staff_email(email):
    staff=Staff.query.filter_by(email=email).first()
    if (staff):
        return staff
    return None


def search_staff(staff_id):
    found = Staff.query.filter_by(staff_id=staff_id).first()
    if(found):
        return found
    else:
        return None    


def create_student(studentID, firstname, lastname, contact, studentType, program):
    new_student = Student(studentID=studentID, firstname=firstname, lastname=lastname, contact=contact, studentType=studentType, program=program)
    
    if new_student:
        db.session.add(new_student)
        db.session.commit()
        return new_student
    return None


def search_students_searchTerm(staff, searchTerm):
    students = staff.searchStudent(searchTerm)
    if students:
      return students
    return None


def create_staff(staffID, email, firstname, lastname, password, te):
    new_staff = add_staff(staffID, email, firstname, lastname, password, te)
    return new_staff

def add_staff(staff_id, email, firstname, lastname, password, teachingExperience):
    new_staff = Staff(staff_id=staff_id, email=email, firstname=firstname, lastname=lastname, password=password, teachingExperience=teachingExperience)

    db.session.add(new_staff)
    db.session.commit()
    
    return new_staff

def editStaff(firstname, lastname, email, password, te):
    staff = search_staff(staff_id)
    if self == staff:
        staff.firstname = firstname
        staff.lastname = lastname
        staff.email = email
        staff.password = password
        staff.teachingExperience = te
        db.session.add(staff)
        db.session.commit()
        return staff
    return None
