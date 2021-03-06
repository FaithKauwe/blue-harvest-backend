from app import db



class DailyTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_id is FK to User table
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime, nullable = False) 
    sleep = db.Column(db.Integer)
    exercise = db.Column(db.Integer)
    caffeine = db.Column(db.Integer)
    alcohol = db.Column(db.Integer)
    water = db.Column(db.Integer)
    stress = db.Column(db.Integer)
    headache = db.Column(db.Integer)
    nausea = db.Column(db.Integer)
    ibs = db.Column(db.Integer)
    dizzy = db.Column(db.Integer)
    energy = db.Column(db.Integer)
    seasonal_illness = db.Column(db.Integer)
    # user is the relationship to user table and there will now be a new attribute created 
    # through backref, user.days
    
    meals = db.relationship("Meal", backref= "day")
    
    

    
