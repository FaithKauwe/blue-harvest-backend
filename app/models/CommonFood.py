from app import db
from app.models.meal import Meal

class CommonFood(db.Model):
    # building the database table with columns, data type, column names
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable = False)
    ingredients = db.Column(db.String)
    
