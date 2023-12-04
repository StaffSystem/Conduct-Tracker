import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
import random
from App.controllers.review import get_reviews_of_student
from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Staff, Admin
from App.controllers import (
    create_user,
    get_karma_by_id,
    create_student,
    jwt_authenticate,
    get_student,
    get_staff,
    create_staff, 
    update_student,
    create_review, 
    editReview, 
    deleteReview, 
    get_review, 
    search_students_searchTerm
)
from App.models.VotingStrategy import DownVote


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''

#run tests with "pytest App/tests/test_app.py" command in shell

class UserUnitTests(unittest.TestCase):

    def test_new_admin (self):
        newAdmin = Admin("Bob", "Boblast",  "bobpass")
        assert newAdmin.firstname == "Bob" and newAdmin.lastname == "Boblast"

    def test_new_staff (self):
        newStaff = Staff( staff_id="342", firstname="Bob", lastname="Charles", password="bobpass", email="bob.charles@staff.com", teachingExperience="10")
        assert newStaff.firstname == "Bob" and newStaff.lastname == "Charles" and newStaff.check_password("bobpass") and newStaff.staff_id == "342" and newStaff.email == "bob.charles@staff.com" and newStaff.teachingExperience == "10"

    def test_new_student (self):
        newStudent = Student( studentID="813", firstname="Joe", lastname="Dune",contact= "0000-653-4343",studentType= "Full-Time",program= "2")
        if newStudent:
        
            assert newStudent.ID == "813" and newStudent.firstname == "Joe" and newStudent.lastname == "Dune" and newStudent.contact == "0000-653-4343" and newStudent.studentType == "Full-Time" and newStudent.program == "2"

    def test_set_password(self): 
        newAdmin = Admin("Bob", "Boblast",  "bobpass")
        password = newAdmin.password
        assert newAdmin.set_password("tompass") != password and newAdmin.check_password != password

    def test_check_password(self): 
        newAdmin = Admin("Bob", "Boblast",  "bobpass")
        assert newAdmin.check_password("bobpass") != "bobpass"

    def test_admin_to_json(self): 
        newAdmin = Admin("Bob", "Boblast",  "bobpass")
        newAdmin_json = newAdmin.to_json()
        self.assertDictEqual(newAdmin_json, {"adminID":"A1", "firstname":"Bob", "lastname":"Boblast"})


    # pure function no side effects or integrations called
    def test_get_json(self):
        user = Admin("bob", "boblast",  "bobpass")
        user_json = user.to_json()
        self.assertDictEqual(user_json, {"adminID":"A1", "firstname":"bob", "lastname":"boblast"})
    
    def test_hashed_password(self):
        password = "mypass"
        user = Admin("bob", "boblast",  password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = Admin("bob", "boblast",  password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


class UsersIntegrationTests(unittest.TestCase):
    # def test_authenticate_admin(self): 
    #     newAdmin = create_user("bob", "boblast", "bobpass")
    #     token = jwt_authenticate(newAdmin.ID, "bobpass")
    #     assert token is not None
    
    def test_create_student(self):
        newAdmin = create_user("rick", "rolast", "bobpass")
        newStudent = create_student(studentID= "813",firstname= "Joe", lastname="Dune", contact="0000-653-4343",studentType= "Full-Time", program= "2")
        assert newAdmin.firstname == "rick" and newAdmin.lastname == "rolast" and newAdmin.check_password("bobpass")
        assert newStudent.ID == "813" 
        assert newStudent.firstname == "Joe" 
        assert newStudent.lastname == "Dune" 
        assert newStudent.contact == "0000-653-4343" 
        assert newStudent.studentType == "Full-Time" 
        assert newStudent.program == "2"

    def test_create_staff(self):
        #newAdmin = create_user("bobby", "bobblast", "bobpass")
        newStaff = create_staff( firstname="Bob", lastname="Charles",password= "bobpass",staffID= "342", email="bob.charles@staff.com",te= "10")
        #assert newAdmin is not None
        assert newStaff.firstname == "Bob" 
        assert newStaff.lastname == "Charles" 
        assert newStaff.check_password("bobpass") 
        assert newStaff.staff_id == "342" 
        assert newStaff.email == "bob.charles@staff.com" 
        assert newStaff.teachingExperience == 10

    def test_search_students(self):
        staff = get_staff(342)
        assert search_students_searchTerm(staff, "Joe") is not None

    # def test_authenticatne_staff(self): 
    #     newAdmin = create_user ("tom", "tomlast", "tompass")
    #     newStaff = create_staff(newAdmin, "Bobby", "Charls", "bobbpass", "343", "bobby.charls@staff.com", "10")
    #     token = jwt_authenticate(newStaff.ID, "bobbpass")
    #     assert newAdmin is not None
    #     assert newStaff is not None
    #     assert token is not None 
    
    def test_update_student(self): 
        student = get_student("813") 
        oldFirstname = student.firstname
        oldLastname = student.lastname 
        oldContact = student.contact 
        oldStudentType = student.studentType
        oldYearOfStudy = student.program
        update_student(student.student_id, "Tom", "Jerry")
        assert student.firstname != oldFirstname and student.firstname == "Joey"
        assert student.lastname != oldLastname and student.lastname == "Dome"
        # assert student.contact != oldContact and student.contact == "0000-123-4567"
        # assert student.studentType != oldStudentType and student.studentType == "Part-Time"
        # assert student.program != oldYearOfStudy and student.program== 5

    def test_create_review(self): 
        admin = create_user("rev", "revlast", "revpass")
        staff = create_staff(firstname="Jon", lastname="Den", password="password", staffID= "546", email="john@example.com",te= 5)
        student = create_student(studentID="2", firstname="Jim", lastname="Lee", contact="000-144-4145", studentType="Full-time",program= "1")
        review = create_review(staffID=staff.ID,studentID= student.ID, is_positive=True, comment="This is a great review")
        assert admin and staff and student
        assert review.reviewerID == staff.ID
        assert review.studentID == student.ID
        assert review.isPositive == True 
        assert review.comment == "This is a great review"

    def test_edit_review(self): 
        admin = create_user("grey", "graylast", "graypass")
        staff = create_staff("Ben", "Gen", "password", "756", "ben@example.com", 7)
        student = create_student("456", "Kim", "Qee","kim@school.com", "Part-time", 4)
        review = create_review(staff.ID, student.ID, True, "This is a great review")
        oldReviewIsPositive = review.isPositive
        oldReviewComment = review.comment
        editReview(review, staff, False, "This is a good review of a horrible student")
        assert admin and staff and student and review 
        assert review.isPositive != oldReviewIsPositive
        assert review.comment != oldReviewComment

    def test_delete_review(self): 
        admin = create_user("Green", "greenlast", "greenpass")
        staff = create_staff("Pem", "Ven", "password", "777", "pem@example.com", 6)
        student = create_student("666", "Cem", "Sem", "cem@school.com", "Part-time", 4)
        review = create_review(staff.ID, student.ID, True, "Soon to be deleted")
        assert admin and staff and student and review 
        deleteReview(review, staff)
        assert get_review(review.ID) is None 

    def test_get_reviews_for_student(self): 
        admin = create_user("Red", "redlast", "redpass")
        staff = create_staff(admin, "Xem", "Zenm", "password", "111", "zenm@example.com", 6)
        student = create_student(admin, "222", "Demn", "Sam", "pass01234", "demn@school.com", "Evening", 2)
        assert admin and staff and student
        assert create_review(staff.ID, student.ID, True, "What a good student")
        assert create_review(staff.ID,  student.ID, True, "He answers all my questions in class")
        reviews = get_reviews_of_student(student.ID)
        for review in reviews: 
            assert review.studentID == student.ID 

    def test_get_reviews_by_staff(self): 
        admin = create_user("Blue", "bluelast", "bluepass")
        staff = create_staff(admin, "Forg", "Qu", "password", "3333", "qu@example.com", 4)
        student = create_student(admin, "1111", "Ano", "One", "pass01234", "sigh@school.com", "Full-Time", 6)
        assert admin and staff and student
        assert create_review(staff.ID, student.ID, False, "What a bad student")
        assert create_review(staff.ID,  student.ID, False, "He always talk during class")
        reviews = get_reviews_by_staff(staff.ID)
        for review in reviews: 
            assert review.reviewerID == staff.ID 

    # def test_upvote(self):
    #     admin = create_user("White", "whitelast", "whitepass")
    #     staff_1 = create_staff("Geo", "Twin1", "password", "5555", "twin1@example.com", 8)
    #     staff_2 = create_staff("Geo", "Twin2", "password", "4444", "twin2@example.com", 8)
    #     student = create_student("9999", "Kil", "Me", "pass01234", "void@school.com", "Full-Time", 4)
    #     review = create_review(staff_1.ID, student.ID, True, "Do i even need to review this student")
    #     assert admin and staff_1 and staff_2 and student and review
    #     old_upVotes = review.upvotes
    #     old_downvotes = review.downvotes
    #     assert old_upVotes + 1 == upvote_Review(review.ID, staff_2) 
    #     assert old_downvotes == review.downvotes

    # def test_downvote(self):
    #     admin = create_user("Black", "blacklast", "blackpass")
    #     staff_1 = create_staff("Geo", "Twin3", "password", "6666", "twin3@example.com", 8)
    #     staff_2 = create_staff("Geo", "Twin4", "password", "7777", "twin4@example.com", 8)
    #     student = create_student("9998", "Still", "Here", "null@school.com", "Full-Time", 5)
    #     review = create_review(staff_1.ID, student.ID, False, "Do i even need to review this horrible thing called a student")
    #     downVote= DownVote()
        
    #     assert admin and staff_1 and staff_2 and student and review
    #     old_upVotes = review.upvotes
    #     old_downvotes = review.downvotes
    #     assert old_upVotes == review.upvotes
    #     assert old_downvotes + 1== downVote.vote(review)
        #assert old_downvotes + 1 == downvoteReview(review.ID, staff_2) 

    # def test_get_rankings(self): 
    #     admin = create_user("Brown", "brownlast", "brownpass")
    #     assert admin
    #     for student in range (2011, 2021): 
    #         assert create_student(admin, student, "Fname" + str(student), "Lname" + str(student), "password", "0000-123-4567", "Full-Time", 2)
    #     for staff in range (2000, 2010):
    #         assert create_staff(admin, "Fname" + str(staff), "Lname" + str(staff), "password2", staff, str(staff) + "email@example.com", 5)
    #         assert create_review(staff, staff + 11, random.choice([True, False]), "reviewing...") 
    #     for staff in range (2000, 2010):
    #         reviews = get_reviews_by_staff(staff)
    #         assert reviews 
    #         for review in reviews: 
    #             for voter in range (2000, 2010):
    #                 if get_staff(voter).ID != review.reviewerID: 
    #                     assert random.choice([upvoteReview(review.ID, get_staff(voter)), downvoteReview(review.ID, get_staff(voter))])
    #     assert get_student_rankings(get_staff(2000)) is not None

    def test_get_karma_score_by_id(self): 
        assert get_karma_by_id(1).karmaID == 1
