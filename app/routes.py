
from flask import Blueprint, jsonify, request, make_response

from app import db
from datetime import datetime, timedelta

from app.utilities import validate_request_body

# assign videos_bp to the new Blueprint instance
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
# beginning CRUD routes/ endpoints for videos
@videos_bp.route("", methods=["POST"])
def post_one_video():
    # request_body will be the user's input, converted to json. it will be a new record 
    # for the db, with all fields (a dict)
    request_body = request.get_json()
    # this guard clause will give an error if user tries to submit request body that does
    # not have all fields present
    if 'title' not in request_body:
        return make_response({"details": "Request body must include title."}, 400)
    elif 'release_date' not in request_body:
        return make_response({"details": "Request body must include release_date."}, 400)
    elif 'total_inventory' not in request_body:
        return make_response({"details": "Request body must include total_inventory."}, 400)
    else:
        # taking info fr request_body and converting it to new Video object    
        new_video = Video(title=request_body["title"],
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"])
        # committing changes to db
        db.session.add(new_video)
        db.session.commit()
        # return formatted response body
        return make_response({ "id": new_video.id,
                                        "title": new_video.title,
                                        "release_date": new_video.release_date,
                                        "total_inventory": new_video.total_inventory}, 201)

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    # querying db for all videos and ordering them by title, then storing that list of 
    # objects in local videos variable    
    videos = Video.query.order_by(Video.title).all()
    videos_response = []
    # looping through eachvideo, converting to requested format (dict) and adding to
    # videos_response which will be list of dicts
    for video in videos:    
        videos_response.append({
        'id':video.id,
        'title':video.title,
        'release_date':video.release_date,
        'total_inventory':video.total_inventory
        })
    
    return jsonify(videos_response), 200

@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE", "PATCH"])
def CRUD_one_video(video_id):
    # this is a guard clause to make sure a video_id is an int, or can be converted to an int    
    try:
        int(video_id)
    except ValueError:
        return make_response({"details": "video_id must be valid integer"}, 400)
    video = Video.query.get(video_id) #either get Video back or None, video here is an object
    if video is None:
        return make_response({"message": f"Video {video_id} was not found"}, 404)
    # returning the object's info in the desired data structure format    
    if request.method == "GET":        
        return make_response({"id": video.id,
                        "title": video.title,
                        "release_date": video.release_date,
                        "total_inventory": video.total_inventory}, 200)
    # PUT will replace the entire record with an entire new record, all fields
    elif request.method == "PUT":
        # form data is a local variable to hold the body of the HTTP request
        form_data = request.get_json()
        # checking that form_data has all required fields
        if "title" not in form_data or "release_date" not in form_data \
        or "total_inventory" not in form_data:
            return make_response({"details": "all fields must be present"}, 400)

    # reassigning attributes of the video object using the dict values that came over 
    # in the request body
        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]

        db.session.commit()

        return make_response({"id": video.id,
                        "title": video.title,
                        "release_date": video.release_date,
                        "total_inventory": video.total_inventory}, 200)
    # PATCH will change just one part of the record, not the whole record
    # not required but adding a patch for total_inventory on 11.9.21
    elif request.method == "PATCH":
        form_data = request.get_json()
        if "total_inventory" in form_data:
            video.total_inventory = form_data["total_inventory"]
        db.session.commit()
        return make_response({"video": {"id": video.id,
                        "title": video.title,
                        "release_date": video.release_date,
                        "total_inventory": video.total_inventory}}, 200)
    elif request.method == "DELETE":
        # if the video has outstanding rentals, don't delete and send message stating there are outstanding rentals
        if Rental.query.filter_by(video_id=video_id, checked_in=False).count() > 0:
            return jsonify({"message": f"Video {video_id} has outstanding rentals"}), 200
        db.session.delete(video)
        db.session.commit()
        return make_response({'id': video.id}, 200)
    
# begin endpoints/ functions for Customer Model
customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

def make_customer_dict(customer): 
    return {
        "id" : customer.id,
        "name" : customer.name,
        "postal_code" : customer.postal_code,
        "phone" : customer.phone,
        "registered_at" : customer.registered_at,
        } 

@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():
    if request.method == "GET":       
        customers = Customer.query.all()

        customers_response = []
        for customer in customers:
            current_customer = make_customer_dict(customer)
            customers_response.append(current_customer)
            
        return jsonify(customers_response), 200
    # POST
    else: 
        request_body = request.get_json()
        valid, missing_attributes = validate_request_body(request_body, ["postal_code", "phone", "name"])
        if valid != True:
            return {"details": f"Request body must include {missing_attributes[0]}."}, 400
        # if all required values are given in the request body, return the video info with 201
        else: 
            new_customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"],
            registered_at=datetime.now()
        )
        db.session.add(new_customer)
        db.session.commit()

        return make_customer_dict(new_customer), 201

@customers_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
def handle_one_customer(id):
    try:
        int_id = int(id)
    except ValueError:
        return jsonify(""), 400

    customer = Customer.query.get(id)
    
    # Guard clause 
    if customer is None:
        return jsonify({"message": (f'Customer {id} was not found')}), 404
    
    
    if request.method == "GET": 
        return jsonify(make_customer_dict(customer)), 200
        
    elif request.method == "PUT":
        form_data = request.get_json()
        valid, missing_attributes = validate_request_body(form_data, ["postal_code", "phone", "name"])

        if valid != True:
            return jsonify(f"Request body missing {missing_attributes[0]}"), 400

        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]

        db.session.commit()
        return jsonify(make_customer_dict(customer)), 200

    elif request.method == "DELETE":
        # if the customer has outstanding rentals, don't delete and send message stating there are outstanding rentals
        if Rental.query.filter_by(customer_id=id, checked_in=False).count() > 0:
            return jsonify({"message": f"Customer {customer.id} has outstanding rentals"}), 200
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"id": customer.id}), 200

# begin endpoints/ functions for Rental Model
# create rentals_bp, a new instance of Blueprint
rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def check_out_one_rental():
    # request_body will be the user's input, converted to json. it will be a new record 
    # for the db, with 2 fields (a dict)    
    request_body = request.get_json()
    valid, missing_attributes = validate_request_body(request_body, ["video_id", "customer_id"])
    # return 400 if video_id or customer_id is missing
    if valid != True:
            return jsonify({"details": "Invalid data"}), 400

    timestamp = datetime.now()
    due_date = timestamp + timedelta(weeks=1)
    # getting the specific video object to access its attributes
    video = Video.query.get(request_body["video_id"])

    if video == None:
        return jsonify(""), 404

    # create available inventory count before rented_vids updates it
    # if no movies are available, return 400
    available_vids = video.available_inventory() 
    if available_vids == 0:
        return jsonify({"message": "Could not perform checkout"}), 400

    #checking for valid customer id
    customer = Customer.query.get(request_body["customer_id"])

    # checks for validity of video id and customer id
    if video and customer:
        # customer_id and video_id both come fr request_body, due_date is calculated with timedelta  
        # checked_in starts as False bc the first time this record is created is when vid is checked out
        new_rental = Rental(customer_id = request_body["customer_id"], 
                            video_id = request_body["video_id"],
                            checked_in = False,
                            due_date = due_date)

        db.session.add(new_rental)
        db.session.commit()
        # begin checked_out calculations after db commit to include most recent rental    
        #rented_vids is list of objects matching request_body["video_id"] AND not marked as checked_in

        available_inventory = video.available_inventory() 
        rented_vids = video.video_checked_out_count()

        return jsonify({"customer_id": new_rental.customer_id,
                                            "video_id": new_rental.video_id,
                                            "due_date": new_rental.due_date,
                                            "videos_checked_out_count": rented_vids,
                                            "available_inventory": available_inventory}), 200

    else: 
        return jsonify(""), 404

@rentals_bp.route("/check-in", methods=["POST"])
def check_in_one_rental():
    request_body = request.get_json()
    # return 400 if video_id or customer_id is missing
    valid, missing_attributes = validate_request_body(request_body, ["video_id", "customer_id"])
    # return 400 if video_id or customer_id is missing
    if valid != True:
            return jsonify({"details": "Invalid data"}), 400
    
    # getting the specific video object to access its attributes
    video = Video.query.get(request_body["video_id"])

    # if there aren't any videos that match the query, return 404
    if video == None:
        return jsonify(""), 404

    #gets the customer object to access its attributes
    customer = Customer.query.get(request_body["customer_id"])

    # checks for validity of video id and customer id
    if video and customer:
        # rental query is one specific object that matches the given parameters 'video_id' and 'customer_id'
        # in order to access the object from the query and perform pythonic methods on it, etc., you need to add the .first() function 
        rental_query = Rental.query.filter_by(video_id=request_body["video_id"], customer_id=request_body["customer_id"],checked_in= False).first()
        # if there isn't a rental matching the given parameters, return 400
        if rental_query == None:
            return jsonify({"message": f"No outstanding rentals for customer {customer.id} and video {video.id}"}), 400

        # changed "checked_in" to True and "due_date" to None/null
        rental_query.checked_in = True
        rental_query.due_date = None

        db.session.commit()

        # calls helper function in Customer to access the num of videos the customers has checked out
        num_customer_videos = customer.customers_checked_out_videos()
        # calls helper function in Video to get the inventory of the specific movie
        available_inventory = video.available_inventory()

        return jsonify({"customer_id": rental_query.customer_id,
                        "video_id": rental_query.video_id,
                        "videos_checked_out_count": num_customer_videos,
                        "available_inventory": available_inventory}), 200
    else:
        # if video or customer doesn't exist, return 404
        return jsonify(""), 404

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def current_vids_customer_checked_out(customer_id):
    
    customer_query = Customer.query.filter_by(id=customer_id).first()
    # guard clause checking if the customer_id exists in Customer table
    if customer_query :
        # checked_out_vids is list of Rental objects fitting query params, but this will only  provide us with due_date
        # to get title and release_date, need to access Video table
        checked_out_vids = Rental.query.filter_by(customer_id=customer_id,checked_in= False).all()
        rentals_response = []
        # looping through each rental, converting to requested format (dict) and adding to
        # videos_response which will be list of dicts
        # bc we created relationship between Rental and Video in rental.py, now we can access Video attributes
        # through dot notation, gets chained to rental.
        for rental in checked_out_vids:    
            rentals_response.append({
            'title':rental.video.title,
            'release_date':rental.video.release_date,
            'due_date':rental.due_date
            })
        return jsonify(rentals_response), 200
    else:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def all_customers_with_vid_checked_out(video_id):
    video_query = Video.query.filter_by(id=video_id).first()
    if video_query :
        # customers_with_vid is list of Rental objects fitting query params, but this will only  provide us with due_date
        # to get name, phone, postal_code, need to access Customer table
        customers_with_vid = Rental.query.filter_by(video_id=video_id,checked_in= False).all()
        # customer_response is a list of dicts
        customers_response =[]
        for rental in customers_with_vid:
            customers_response.append({
            'name':rental.customer.name,
            'phone':rental.customer.phone,
            'postal_code':rental.customer.postal_code,
            'due_date':rental.due_date
            })
        return jsonify(customers_response), 200
    else:
        return jsonify({"message": f"Video {video_id} was not found"}), 404


   
                                    



                                
    


