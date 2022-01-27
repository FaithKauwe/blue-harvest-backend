from app import db


class CommonFood(db.Model):
    # building the database table with columns, data type, column names
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable = False)
    ingredients = db.Column(db.String(50))
    
    meals = db.relationship("Meal", backref= "food")
    
