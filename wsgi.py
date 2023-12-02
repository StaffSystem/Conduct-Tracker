from flask_login import current_user, login_required
from flask_jwt_extended import current_user as jwt_current_user
from App.controllers.review import get_review, get_reviews
from App.controllers.staff import create_review
from App.models import Upvote
from App.models.review import Review
from App.models.staff import Staff
from App.models.student import Student
from App.views.index import generate_random_contact_number
import click, pytest, sys
from flask import Flask, jsonify
from flask.cli import with_appcontext, AppGroup
import random
import randomname
from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, create_staff, create_student, get_all_users_json, get_all_users )
from App.views import (generate_random_contact_number)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  admin= create_user('bob', 'boblast' , 'bobpass')
  for ID in  range(2, 50): 
    staff= create_staff( 
          randomname.get_name(), 
          randomname.get_name(), 
          randomname.get_name(), 
          str(ID), 
          randomname.get_name() + '@schooling.com', 
          str(random.randint(1, 15))
      )
    db.session.add(staff)
    db.session.commit()
    
    

  for ID in range(50, 150): 
      contact= generate_random_contact_number()
      student= create_student(str(ID),
          randomname.get_name(), 
          randomname.get_name(), 
          contact,
          random.choice(['Full-Time','Part-Time', 'Evening']),
          "Bsc ComputerScience"
      )
      db.session.add(student)
      db.session.commit()
  print("Database Initialised")
  return jsonify({'message': 'Database initialized'}),201

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("firstname", default="rob")
@click.argument("password", default="robpass")
def create_user_command(firstname, password):
    create_user(firstname, password)
    print(f'{firstname} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


app.cli.add_command(test)

systemTest = AppGroup("system", help='User Interface')

#flask system login
@systemTest.command("loginStaff")
@click.argument("email", default="bob@com")
@click.argument("password", default="bobpass")
def Login(email,password):
    staff = login(email, password)
    if staff:
        print(f'Sucessfully logged in: {staff.firstname} {staff.lastname}')


#flask system logout
@systemTest.command("logoutStaff")
def Logout():
    pass


#flask system addStudent
@systemTest.command("addStudent")
def addStudent():
    print("Student Added")
    pass


#flask system searchStudent
@systemTest.command("searchStudent")
@click.argument("student_id", default= "1")
def SearchStudent(student_id):
    student = get_student(student_id)
    if student: 
        print(f'Student found: {student.firstname} {student.lastname}!')
    else:        
        print("Student not found")


#flask system editStudent
@systemTest.command("editStudent")
def EditStudent():
    print("Student Successfully edited")
    pass


# @systemTest.command("addstaff")
# @click.argument("firstname", default="rib")
# @click.argument("lastname", default="ribby")
# @click.argument("password", default="ribpass")
# @click.argument("staffid", default="RIB22")
# @click.argument("email", default="rIb@gmail.com")
# @click.argument("te", default=1)
# #staffID=ID,firstname=firstname,lastname=lastname,password=password,email=email,te=teacherExperience
# def addStaff(staffid,email,firstname,lastname,password,te):
#     staff=create_staff(staffid,email,firstname,lastname,password,te)
#     if staff:
#         print("Staff Added")
#         return staff
#     return None


#flask system searchStaff
@systemTest.command("searchStaff")
@click.argument("staff_id", default="1")
def SearchStaff(staff_id):
    found = search_staff(staff_id)
    if found:
        print(f'Staff found: {found.firstname} {found.lastname}!')
    else:
        print("Staff not found")


# #flask system editStudent
# @systemTest.command("editStaff")
# def EditStaff():
#     staff = editStaff(firstname, lastname, email, password, te)
#     print("Student Successfully edited")
#     pass


#flask system createReview
# @systemTest.command("createReview")
# @click.argument("studentid", default="1")
# @click.argument("username", default="Rib")
# @click.argument("ispositive", default="True")
# @click.argument("comment", default="Very Good")
# def CreateReview(studentid,username,ispositive, comment):
#     student=Student.query.filter_by(ID=studentid).first()
#     staff=Staff.query.filter_by(firstname=username)
#     review=create_review(staffid=staff.staffid,studentid=studentid,ispositive=ispositive,comment=comment)
#     if review:
#         print("Review Created")
#     return None


#flask system getReview
#get all reviews
@systemTest.command("getReviews")
@click.argument("studentid", default="1")
def GetReviews(studentid):
    reviews = get_reviews_of_student(studentID)
    if reviews:
        print("Reviews retrieved")
    else:
        print("No reviews found")


#get specific review
@systemTest.command("getReview")
@click.argument("reviewID", default="1")
def GetReview(reviewID):
    review = get_review(reviewID)
    if review:
        print("Review retrieved")
    else:
        print("No review was found")


#flask system editReview
@systemTest.command("editReview")
@click.argument("reviewid")
@click.argument("staffid")
@click.argument("is_positive", default="true")
@click.argument("comment", default="test")
def editReview(reviewid, staffid, is_positive, comment):
    reviewfound = get_review(reviewid)
    stafffound = search_staff(staff_id)
    rev = editReview(review, staff, is_positive, comment)
    if rev:
        print("Review Edited")


#flask system deleteReview
@systemTest.command("deleteReview")
@click.argument("reviewid")
@click.argument("staffid")
def DeleteReview(review, staff):
    review = get_review(reviewid)
    staff = search_staff(staff_id)
    dele = deleteReview(review, staff)
    if dele: 
        print("Review Deleted")
    

#flask system vote
@systemTest.command("vote")
@click.argument("reviewid", default="1")
def Vote(reviewid):
    review=Review.query.get(reviewid)
    if review:
        
        print("Voted")
    return None



app.cli.add_command(systemTest)


# cli command: flask vote upvote
reviewTest = AppGroup('vote', help='Testing') 
@reviewTest.command("upvote")

def voteTest():
    staff=Staff(staffID="mich22",firstname="Mich",lastname="Jerry",password="michpass",email="mich@gmail.com",teachingExperience=4)
    student=Student(studentID="S21",firstname="Bob",lastname="bobby",contact="423-124",studentType="Full",program="Computer Science")
    review= Review(reviewer=staff,student=student, isPositive=True, comment="Very good")
    print("Hello before")
    upvote=Upvote()
    upvote.vote(review)
    print("Hello after")
    pass
  
app.cli.add_command(reviewTest)