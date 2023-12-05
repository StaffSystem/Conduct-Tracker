from App.database import db
from .user import User
from datetime import datetime

class Student(db.Model):
	__tablename__ = 'student'
	ID = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(120), nullable=False)
	lastname = db.Column(db.String(120), nullable=False)
	contact = db.Column(db.String(30), nullable=False)
	studentType = db.Column(db.String(30))  #full-time, part-time or evening
	program = db.Column(db.String(120), nullable=False)
	programBegan = db.Column(db.DateTime, default=datetime.utcnow)
	reviews = db.relationship('Review', backref='student', lazy='joined')
	karma = db.Column(db.Float, nullable=True)

  #When student is newly created there would be no reviews or karma yet
	def __init__(self, studentID, firstname, lastname, contact, studentType, program):
		self.firstname = firstname
		self.lastname = lastname
		self.contact = contact
		self.karma=0.00
		self.studentType = studentType
		self.program = program
		self.reviews = []
	
	def get_id(self):
		return self.ID

#Gets the student details and returns in JSON format
	def to_json(self):
		return {
        "studentID": self.ID,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "contact": self.contact,
        "studentType": self.studentType,
        "programBegan": self.programBegan,
        "reviews": [review.to_json() for review in self.reviews], 
		"karmaScore": self.karma
    }

#get karma record from the karma table using the karmaID attached to the student
	def getKarma(self):
		from .karma import Karma
		return Karma.query.get(self.karmaID)

	def edit_name(self, fname, lname):
		self.firstname = fname
		self.lastname = lname

		db.session.commit()
