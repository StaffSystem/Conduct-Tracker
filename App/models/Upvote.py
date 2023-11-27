from App.models import VotingStrategy

class Upvote(VotingStrategy):
    # implementation of Upvote method
    def vote(staff):
        if staff in self.staffUpvoters:  # if they upvoted the review already, return current votes
            return self.upvotes
        else:
            if staff not in self.staffUpvoters:  #if staff has not upvoted allow the vote
                self.upvotes += 1
                self.staffUpvoters.append(staff)

                if staff in self.staffDownvoters:  #if they had downvoted previously then remove their downvote to account for switching between votes
                    self.downvotes -= 1
                    self.staffDownvoters.remove(staff)    

        db.session.add(self)
        db.session.commit()

        return self.upvotes

