from app import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(50), nullable = False)
    days = db.relationship("DailyTracker", backref= "user")