from App.database import db

class State():
    ID = db.Column(db.Integer, primary_key=True)
    staffID=db.Column(db.String(10), db.ForeignKey('staff.ID'))
    messsage=db.Column(db.String(100),nullable=True)
    
    