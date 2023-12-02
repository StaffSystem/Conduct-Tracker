from abc import ABC, abstractmethod
from App.database import db
from App.models import staff

class VotingStrategy(ABC):
    @abstractmethod
    def vote(self,review):
        pass
    
    
class Upvote(VotingStrategy):
    def vote(self,review):
        print("IN UPVOTE")
        if review in review.reviewUpvoters:  # if they upvoted the review already, return current votes
            return review.upvotes
        else:
            if review not in review.reviewUpvoters:  #if review has not upvoted allow the vote
                review.upvotes += 1
                review.reviewUpvoters.append(review)

                if review in review.reviewDownvoters:  #if they had downvoted previously then remove their downvote to account for switching between votes
                    review.downvotes -= 1
                    review.reviewDownvoters.remove(review)    

        db.session.add(review)
        db.session.commit()

        return review.upvotes
    
    from App.models import VotingStrategy

class DownVote(VotingStrategy):
    # implementation of Downvote method
    def vote(self,review):
        if staff in review.staffDownvoters:  # If they downvoted the review already, return current votes
            return review.downvotes
        else:
            if staff not in review.staffDownvoters:  #if staff has not downvoted allow the vote
                review.downvotes += 1
                review.staffDownvoters.append(staff)

                if staff in review.staffUpvoters:  #if they had upvoted previously then remove their upvote to account for switching between votes
                    review.upvotes -= 1
                    review.staffUpvoters.remove(staff)
        
        db.session.add(review)
        db.session.commit()

        return review.downvotes