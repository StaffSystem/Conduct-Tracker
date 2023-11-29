from App.database import db
from .user import User
from datetime import datetime

class Student(db.Model):
	__tablename__ = 'student'
	ID = db.Column(db.String(10), primary_key=True)
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
		self.ID = studentID
		self.firstname = firstname
		self.lastname = lastname
		self.contact = contact
		self.studentType = studentType
		self.program = program
		self.reviews = []
	
	def get_id(self):
		return self.ID

#Gets the student details and returns in JSON format
	def to_json(self):
		karma = self.getKarma()
		return {
        "studentID": self.ID,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "contact": self.contact,
        "studentType": self.studentType,
        "programBegan": self.programBegan,
        "reviews": [review.to_json() for review in self.reviews], 
		"karmaScore": karma.score if karma else None,
    }

#get karma record from the karma table using the karmaID attached to the student
	def getKarma(self):
		from .karma import Karma
		return Karma.query.get(self.karmaID)
