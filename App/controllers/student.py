from App.models import Student
from App.database import db

def search_student(studentID):
    student = db.session.query(Student).get(studentID)
    if student:
        return student
    return None

def get_student(student_id):
    found_student=Student.query.filter_by(ID=student_id).first()
    
    if(found_student):
        return found_student
    else:
        return None


def update_student(studentID,fname,lname):
    student=Student.query.filter_by(id=studentID).first
    if student:
        student.edit_name(fname,lname);
        # db.session.add(student)
        # db.session.commit()
        return student
    return None

# must edit to reflect change in karma scoring approach
def calculate_student_karma(student):
    good_karma = 0
    bad_karma = 0

    for review in student.reviews:
        if review.isPositive:
            good_karma += review.upvotes
            bad_karma += review.downvotes
        else:
            bad_karma += review.upvotes
            good_karma += review.downvotes

    karma_score = good_karma - bad_karma

    if student.karmaID is not None:
        karma = db.session.query(Karma).get(student.karmaID)
        karma.score = karma_score
    else:
        karma = Karma(score=karma_score)
        db.session.add(karma)
        db.session.flush() 
        student.karmaID = karma.karmaID

    db.session.commit()
    return karma