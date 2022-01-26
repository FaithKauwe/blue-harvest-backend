from app import db
from app.models.DailyTracker import DailyTracker
from app.models.CommonFood import CommonFood

class Meal(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # date_id is the FK to the DailyTracker table (where date_id is DailyTracker's "id")
    date_id = db.Column(db.Integer, db.ForeignKey(DailyTracker.id))
    # food_id is the FK to the CommonFood table (where food_id is CommonFood's "id")
    food_id = db.Column(db.Integer, db.ForeignKey(CommonFood.id))

    #still need to establish relationships with CommonFood and DailyTracker using backref
    
