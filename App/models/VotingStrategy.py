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