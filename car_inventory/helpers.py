from functools import wraps
import secrets
from flask import request, jsonify, json
from car_inventory.models import User
import decimal
import requests

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            our_user = User.query.filter_by(token=token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'})

        except:
            owner = User.query.filter_by(token=token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})
        
        return our_flask_function(our_user, *args, **kwargs)
    
    return decorated

# this car data api only has cars up to 2020
def get_car_type(year,make,model):
    try:

        url = "https://car-data.p.rapidapi.com/cars"

        querystring = {"limit":"1","page":"0","year":f"{year}","make":f"{make}","model":f"{model}"}

        headers = {
            "X-RapidAPI-Key": "0c048494f2msh6d0723a1c767134p1d74eejsnb1f84274613f",
            "X-RapidAPI-Host": "car-data.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response.json()[0]['type']

    except:
        raise Exception(f"Car does not exists in API.")

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)