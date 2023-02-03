from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from ..forms import CarForm
from ..models import Car, db
from ..helpers import get_car_type

site = Blueprint('site', __name__, template_folder = 'site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    my_car = CarForm()
    try:
        if request.method == "POST" and my_car.validate_on_submit():
            year = my_car.year.data.strip()
            make = my_car.make.data.title().strip()
            model = my_car.model.data.title().strip()
            color = my_car.color.data.title().strip()
            car_type = get_car_type(year, make, model)
            user_token = current_user.token

            car = Car(year, make, model, color, car_type, user_token)

            db.session.add(car)
            db.session.commit()

            return redirect(url_for('site.profile'))

    except:
        raise Exception("Could not add car to garage, please check your form and try again!")

    user_token = current_user.token

    cars = Car.query.filter_by(user_token = user_token)

    return render_template('profile.html', form=my_car, cars=cars)