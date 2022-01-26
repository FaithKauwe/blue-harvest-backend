from app import db
from app.models.DailyTracker import DailyTracker


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)