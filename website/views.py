from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import Trip, Sub
from . import db
import json
from datetime import datetime


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    trips = Trip.query.filter_by().all()
    category_dict = {}
    for trip in trips:
        for sub in trip.subs:
            if sub.category not in category_dict:
                category_dict[sub.category] = sub.amount
            else:
                category_dict[sub.category] += sub.amount
    
    return render_template("home.html", user=current_user, category_dict=category_dict)


@views.route('/mytrips', methods=['GET', 'POST'])
@login_required
def mytrips():
    

    return render_template("mytrips.html", user=current_user)


@views.route('/delete-trip', methods=['POST'])
def delete_trip():  
    trip = json.loads(request.data)
    tripId = trip['tripId']
    trip = Trip.query.get(tripId)
    if trip:
        if trip.user_id == current_user.id:
            db.session.delete(trip)
            db.session.commit()
            flash('Trip has been deleted!', category='success')

    return jsonify({})

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    
    return render_template("profile.html", user=current_user)

@views.route('/add-trip', methods=['GET'])
def add_trip():
    
    return render_template("addtrips.html", user=current_user)


@views.route('/save-trip', methods=['GET'])
def save_trip():  
    city = request.args.get('city')
    country = request.args.get('country')
    start = request.args.get('start')
    end = request.args.get('end')
    if len(city) < 1 or len(country) < 1 or len(start) < 1 or len(end) < 1:
        flash('Invalid Input', category='error')
        return redirect('/mytrips') 
    
    duration = calc_dates(start, end)
    new_trip = Trip(city=city, country=country, start_date=start, end_date=end, duration=duration, user_id=current_user.id)
    db.session.add(new_trip)
    db.session.commit()
    flash('Trip has been added!', category='success')
    return redirect('/mytrips')

@views.route('/edit-trip/<int:tripId>', methods=['GET'])
def edit_trip(tripId):
    trip = Trip.query.filter_by(id=tripId).first()
    return render_template("edittrips.html", user=current_user, trip=trip, num_id=tripId)

@views.route('/save-category/<int:tripId>', methods=['GET'])
def save_category(tripId):
    category = request.args.get('category')
    amount = request.args.get('amount')
    if len(category) < 1 or len(amount) < 1:
        flash('Invalid Input', category='error')
        return redirect(f'/edit-trip/{tripId}')
    
    new_sub = Sub(category=category, amount=amount, trip_id=tripId)
    db.session.add(new_sub)
    db.session.commit()
    flash('Sub has been added!', category='success')
    return redirect(f'/edit-trip/{tripId}')

@views.route('/delete-category/<int:subId>', methods=['GET'])
def delete_category(subId):  
    sub = Sub.query.filter_by(id=subId).first()
    if request.method == 'GET':
        if sub:
            print(sub)
            db.session.delete(sub)
            db.session.commit()
            flash('Sub has been deleted!', category='success')
            return redirect(f'/edit-trip/{sub.trip_id}')

    return redirect(f'/edit-trip/{sub.trip_id}')


def calc_dates(date_str_1, date_str_2):
    date_obj_1 = datetime.strptime(date_str_1, '%Y-%m-%d').date()
    date_obj_2 = datetime.strptime(date_str_2, '%Y-%m-%d').date()
    date_diff = date_obj_2 - date_obj_1
    date_diff = str(date_diff)
    
    try:
        idx = date_diff.index("days")
        return (int(date_diff[:idx]) + 1)
    except ValueError:
        if date_obj_1==date_obj_2:
            return 1
        else:
            return 2