# from App.models import VotingStrategy, staff
# from App.database import db

# class Upvote(VotingStrategy):
    
#     # implementation of Upvote method
#     def vote(self,staff):
#         print("IN UPVOTE")
#         # if staff in staff.staffUpvoters:  # if they upvoted the review already, return current votes
#         #     return staff.upvotes
#         # else:
#         #     if staff not in staff.staffUpvoters:  #if staff has not upvoted allow the vote
#         #         staff.upvotes += 1
#         #         staff.staffUpvoters.append(staff)

#         #         if staff in staff.staffDownvoters:  #if they had downvoted previously then remove their downvote to account for switching between votes
#         #             staff.downvotes -= 1
#         #             staff.staffDownvoters.remove(staff)    

#         # db.session.add(staff)
#         # db.session.commit()

#         # return staff.upvotes

