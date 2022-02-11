from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
# from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    
    # import models for Alembic Setup
    from app.models.CommonFood import CommonFood
    from app.models.DailyTracker import DailyTracker
    from app.models.meal import Meal
    from app.models.user import User

    # Setup DB
    db.init_app(app)
    migrate.init_app(app, db)

    #Register Blueprints Here
    from .routes import daily_tracker_bp
    from .routes import meal_bp
    from .routes import common_food_bp
    app.register_blueprint(daily_tracker_bp)
    app.register_blueprint(meal_bp)
    app.register_blueprint(common_food_bp)
    
    # CORS(app)
    return app