
from flask import Blueprint, jsonify, request, make_response

from app import db
from datetime import datetime, timedelta
from app.models.CommonFood import CommonFood
from app.models.meal import Meal
from app.models.DailyTracker import DailyTracker

# assign daily_tracker to the new Blueprint instance
daily_tracker_bp = Blueprint("daily_tracker", __name__, url_prefix="/daily_tracker")
# beginning CRUD routes/ endpoints for daily_tracker

@daily_tracker_bp.route("/<date>", methods=["POST"])
def post_one_day(date):
    request_body = request.get_json()
    # taking info fr request_body and converting it to new DailyTracker object
    new_daily_input = DailyTracker(user_id = 1,
                                date=date,
                                sleep=request_body["sleep"],
                                exercise= request_body["exercise"],
                                caffeine=request_body["caffeine"],
                                alcohol=request_body["alcohol"],
                                water=request_body["water"],
                                stress=request_body["stress"],
                                headache=request_body["headache"],
                                nausea = request_body["nausea"],
                                ibs=request_body["ibs"],
                                dizzy=request_body["dizzy"],
                                energy=request_body["energy"],
                                seasonal_illness=request_body["seasonal"])
    # committing changes to db
    db.session.add(new_daily_input)
    db.session.commit()                            
    return make_response({"details": f"Daily Details for {date} Posted to Tracker"}, 201)
# this get request will return info to the FE data input page to show user what data has already been input 
# for that day
@daily_tracker_bp.route("/<date>", methods=["GET"])
def get_days_data(date):
    data_so_far = DailyTracker.query.filter_by(date=date).first()
    if not data_so_far:
        return jsonify({
                    "food": ["SelectMeal", "SelectMeal", 
                        "SelectMeal", "SelectMeal",
                        "SelectMeal", "SelectMeal"],
                    "sleep":"",
                    "exercise":"",
                    "caffeine":"",
                    "alcohol":"",
                    "water":"",
                    "stress":"",
                    "headache":"",
                    "nausea":"",
                    "ibs":"",
                    "dizzy":"",
                    "energy":"",
                    "seasonal":""})
    meals = data_so_far.meals
    daily_meals=[]
    for meal in meals:
        daily_meals.append(meal.food.name)
    return jsonify({
                    "food":daily_meals,
                    "sleep":data_so_far.sleep,
                    "exercise":data_so_far.exercise,
                    "caffeine":data_so_far.caffeine,
                    "alcohol":data_so_far.alcohol,
                    "water":data_so_far.water,
                    "stress":data_so_far.stress,
                    "headache":data_so_far.headache,
                    "nausea":data_so_far.nausea,
                    "ibs":data_so_far.ibs,
                    "dizzy":data_so_far.dizzy,
                    "energy":data_so_far.energy,
                    "seasonal":data_so_far.seasonal_illness})
@daily_tracker_bp.route("", methods=["GET"])
# this function will get the requested data fr BE based on query options fr FE, package it into data structure
# to be sent back to FE
def get_data_from_query():
    request_body = request.args.to_dict() # getting dict fr user of query params
    symptom = request_body["symptom"].lower()
    if symptom == 'dizziness':
        symptom = 'dizzy'
    elif symptom == 'seasonal illness':
        symptom = 'seasonal_illness'
    print(symptom)
    level = request_body["severity"]
    data_from_query = DailyTracker.query.filter(getattr(DailyTracker, symptom)>level).all()
    requested_data_for_FE={"daily_list":[]}
    for data in data_from_query:
        daily_dict={"date":data.date, symptom:data.nausea}
        if request_body["food"]== True:
            daily_dict["food"]={}
# populating the empty "food" dict by looping through each row and accessing the meal name and ingredients
            for meal in data.meals:
                daily_dict["food"][meal.food.name]=meal.food.ingredients
        if request_body["water"]== True:
            daily_dict["water"]= data.water
        if request_body["alcohol"]== True:
            daily_dict["alcohol"]= data.alcohol
        if request_body["sleep"]== True:
            daily_dict["sleep"]= data.sleep

        requested_data_for_FE["daily_list"].append(daily_dict)
    return make_response(requested_data_for_FE, 200)


# assign meal to the new Blueprint instance
meal_bp = Blueprint("meal", __name__, url_prefix="/meal")
@meal_bp.route("/<date>", methods=["POST"])
def post_one_meal(date):
    request_body = request.get_json() # getting dict fr user of food_name: "oatmeal"
    food_id = CommonFood.query.filter_by(name=request_body["food_name"]).first().id
    date_id = DailyTracker.query.filter_by(date=date).first().id
    new_meal_object = Meal(date_id= date_id,
                            food_id=food_id)
    # committing changes to db
    db.session.add(new_meal_object)
    db.session.commit()  
    return make_response({"details": f"New meal for {date} was logged"}, 201)
@meal_bp.route("/<date>", methods=["GET"])
def get_meals_for_one_date(date):
    daily_id= DailyTracker.query.filter_by(date=date).first().id
    daily_meal_ids= Meal.query.filter_by(date_id=daily_id)
    daily_meals=[]
    for id in daily_meal_ids:
        daily_meals.append(id.food.name)
    return jsonify(daily_meals), 200


common_food_bp = Blueprint("common_food", __name__, url_prefix="/common_food")
@common_food_bp.route("", methods=["POST"])
def post_one_common_food():
    request_body = request.get_json()
    new_common_food = CommonFood(name = request_body["food_name"],
                                ingredients=request_body["ingredients"]) 
    db.session.add(new_common_food)
    db.session.commit()    
    return make_response({"details": f"New common food, {new_common_food.name} posted to CommonFood"}, 201)
# this endpoint will be used by FE to populate the dropdown menu when user is choosing a meal 
@common_food_bp.route("", methods=["GET"])
def get_all_common_foods(): 
    common_foods = CommonFood.query.all() 
    common_foods_for_FE = {}
    for food in common_foods:
        common_foods_for_FE[food.name]=food.ingredients 
    return make_response(common_foods_for_FE, 200) 