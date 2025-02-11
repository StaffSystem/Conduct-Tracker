from App.models import Review, Karma, Student
from App.database import db

def get_reviews(student_id): 
    return db.session.query(Review).all()


def get_reviews_of_student(studentID):
    return Review.query.filter_by(studentID=studentID).all()


def get_review(reviewID):
    return Review.query.filter_by(ID=reviewID).first()


def get_reviews_from_staff(staffID):
    return Review.query.filter_by(reviewerID=staffID).all()


def editReview(review, staff, is_positive, comment):
    if review.reviewer == staff:
        review.isPositive = is_positive
        review.comment = comment
        db.session.add(review)
        db.session.commit()
        return review
    return None


def deleteReview(review, staff):
    if review.reviewer == staff:
        db.session.delete(review)
        db.session.commit()
        return True
    return None


# def downvoteReview(reviewID, staff):
#     review = db.session.query(Review).get(reviewID)
#     if staff in review.staffDownvoters:  # If they downvoted the review already, return current votes
#         return review.downvotes

#     else:
#         if staff not in review.staffDownvoters:  # if staff has not downvoted allow the vote
#             review.downvotes += 1
#             review.staffDownvoters.append(staff)

#             if staff in review.staffUpvoters:  # if they had upvoted previously then remove their upvote to account for switching between votes
#                 review.upvotes -= 1
#                 review.staffUpvoters.remove(staff)

#         db.session.add(review)
#         db.session.commit()
#         # Retrieve the associated Student object using studentID
#         student = db.session.query(Student).get(review.studentID)

#         # Check if the student has a Karma record (karmaID) and create a new Karma record for them if not
#         if student.karmaID is None:
#             karma = Karma(score=0.0, rank=-99)
#             db.session.add(karma)  # Add the Karma record to the session
#             db.session.flush()  # Ensure the Karma record gets an ID
#             db.session.commit()
#             # Set the student's karmaID to the new Karma record's ID
#             student.karmaID = karma.karmaID

#       # Update Karma for the student
#         student_karma = db.session.query(Karma).get(student.karmaID)
#         student_karma.calculateScore(student)
#         student_karma.updateRank()

#     return review.downvotes

# def setStratergy():
    


# def executeStratergy():



