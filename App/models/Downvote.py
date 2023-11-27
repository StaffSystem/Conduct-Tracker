from App.models import VotingStrategy

class DownVote(VotingStrategy):
    # implementation of Downvote method
    def vote(staff):
        if staff in self.staffDownvoters:  # If they downvoted the review already, return current votes
            return self.downvotes

        else:
            if staff not in self.staffDownvoters:  #if staff has not downvoted allow the vote
                self.downvotes += 1
                self.staffDownvoters.append(staff)

                if staff in self.staffUpvoters:  #if they had upvoted previously then remove their upvote to account for switching between votes
                    self.upvotes -= 1
                    self.staffUpvoters.remove(staff)
        
        db.session.add(self)
        db.session.commit()

        return self.downvotes