from app import db
from app.models.DailyTracker import DailyTracker
from app.models.CommonFood import CommonFood

class Meal(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # date_id is the FK to the DailyTracker table (where date_id is DailyTracker's "id")
    date_id = db.Column(db.Integer, db.ForeignKey("day.id"), nullable=False)
    # food_id is the FK to the CommonFood table (where food_id is CommonFood's "id")
    food_id = db.Column(db.Integer, db.ForeignKey("food.id"), nullable=False)

    #still need to establish relationships with CommonFood and DailyTracker using backref
    # in the "day" relationship, "DailyTracker" is a reference point for the relationship to be established but "meals"
    # will be the name that is assigned to the new attribute in DailyTracker class that is created through backref
    day = db.relationship("DailyTracker", backref= "meals")
    food = db.relationship("CommonFood", backref= "meals")
    
