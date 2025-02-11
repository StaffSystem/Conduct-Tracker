from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from .user import User
from .student import Student
from .karma import Karma
from .review import Review

class Staff(db.Model, UserMixin):
  __tablename__ = 'staff'
  ID = db.Column(db.Integer, primary_key=True)
  staff_id = db.Column(db.String(120), nullable=False)
  email = db.Column(db.String(120), nullable=False)
  firstname = db.Column(db.String(120), nullable=False)
  lastname = db.Column(db.String(120), nullable=False)
  password = db.Column(db.String(120), nullable=False)
  teachingExperience = db.Column(db.Integer, nullable=False)

  def set_password(self, password):
    """Create hashed password."""
    self.password = generate_password_hash(password, method='sha256')

  def check_password(self, password):
    """Check hashed password."""
    return check_password_hash(self.password, password)


  def __init__(self, staff_id, firstname, lastname, password, email,teachingExperience):
    self.staff_id = staff_id
    self.email = email
    self.firstname = firstname
    self.lastname = lastname
    self.set_password(password)
    self.teachingExperience = teachingExperience


  def get_id(self):
    return self.ID


  #Retrieve reviews by a staff member from the Review model
  def getReviewsByStaff(self, staff):
    staff_reviews = staff.reviews_created
    return [review.to_json() for review in staff_reviews]


  #create a review for a student
  def createReview(self, staff,student, isPositive, comment):
    review = Review(staff,student, isPositive, comment)
    student.reviews.append(review)  #add review to the student
    db.session.add(review)  #add to db
    db.session.commit()
    return review


  #add student to the database
  def addStudent(self, id, firstname, lastname, contact, studentType, program):
    newStudent = Student(id, firstname, lastname, contact, studentType, program)

    db.session.add(newStudent)
    db.session.commit()
    return newStudent


  def searchStudent(self, searchTerm):
    # Query the Student model for a student by ID or first name, or last name
    students = db.session.query(Student).filter(
        (Student.ID == searchTerm)
        |  #studentID must be exact match (string)
        (Student.firstname.ilike(f"%{searchTerm}%"))
        |  # Search by firstname or lastname - case-insensitive
        (Student.lastname.ilike(f"%{searchTerm}%"))).all()

    if students:
      # If matching students are found, return their json representations in a list
      return [student.to_json() for student in students]
    else:
      # If no matching students are found, return an empty list
      return []

  
  # addstaff to the database
  
  #return staff details on json format
  def to_json(self):
    return {
        "staffID": self.staff_id,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "email": self.email,
        "teachingExperience": self.teachingExperience
    } 

