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
@systemTest.command("login")
def Login():
    pass

#flask system logout
@systemTest.command("logout")
def Logout():
    pass

#flask system createAccount
@systemTest.command("createAccount")
def createAccount():
    print("Account Created")
    pass

#flask system addStudent
@systemTest.command("addStudent")
def addStudent():
    print("Student Added")
    pass

#flask system getData
@systemTest.command("getData")
def getData():
    print("Data Retrieve")
    pass

#flask system dataCopy
@systemTest.command("dataCopy")
def dataCopy():
    print("Data copied")
    pass
#flask system updateData
@systemTest.command("updateData")
def UpdateData():
    print("Data updated")
    pass

#flask system deleteData
@systemTest.command("deleteData")
def DeleteData():
    print("Data deleted")
    pass

#flask system searchStudent
@systemTest.command("searchStudent")
def SearchStudent():
    print("Student Found")
    pass

#flask system editStudent
@systemTest.command("editStudent")
def EditStudent():
    print("Student Successfully edited")
    pass

#flask system createReview
@systemTest.command("createReview")
def CreateReview():
    print("Review Created")
    pass

#flask system getReview
@systemTest.command("getReview")
def GetReview():
    print("Review retrieved")
    pass

#flask system editReview
@systemTest.command("editReview")
def EditReview():
    print("Review Edited")
    pass

#flask system deleteReview
@systemTest.command("deleteReview")
def DeleteReview():
    print("Review Deleted")
    pass

#flask system vote
@systemTest.command("vote")
def Vote():
    print("Voted")
    pass



app.cli.add_command(systemTest)


#cli command: flask vote upvote
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