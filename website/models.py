from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    trips = db.relationship('Trip')


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(150))
    country = db.Column(db.String(150))
    start_date = db.Column(db.String(150))
    end_date = db.Column(db.String(150))
    duration = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subs = db.relationship('Sub', backref='trip')


class Sub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(150))
    amount = db.Column(db.Integer)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
