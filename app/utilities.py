# this is a file of helper functions
def validate_request_body(request_body, list_of_attributes):
    valid = True
    missing_attributes = []
    # for each item in list of attributes, if one is not in request body, valid is false
    for attribute in list_of_attributes:
        if attribute not in request_body:
            missing_attributes.append(attribute)
            valid = False
    return valid, missing_attributes

   
    