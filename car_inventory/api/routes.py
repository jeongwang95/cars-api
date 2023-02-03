from flask import Blueprint, request, jsonify
from car_inventory.helpers import token_required, get_car_type
from car_inventory.models import db, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix = '/api')

# Create car endpoint
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(our_user):
    year = request.json['year'].strip()
    make = request.json['make'].title().strip()
    model = request.json['model'].title().strip()
    color = request.json['color'].title().strip()
    car_type = get_car_type(year,make,model)
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    car = Car(year, make, model, color, car_type, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)

# Retrieve all car endpoint
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(our_user):
    owner = our_user.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)

    return jsonify(response)

# Retrieve one car endpoint
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(our_user, id):
    owner = our_user.token
    if owner == our_user.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid ID Required'}), 401

# Update car endpoint
@api.route('/cars/<id>', methods = ['PUT','POST'])
@token_required
def update_car(our_user, id):
    car = Car.query.get(id)
    car.year = request.json['year']
    car.make = request.json['make']
    car.model = request.json['model']
    car.color = request.json['color']
    car.car_type = get_car_type(car.year,car.make,car.model)
    car.user_token = our_user.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Delete drone endpoint
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(our_user, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)