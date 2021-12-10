from flask_login import UserMixin
from init import db

#user model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

#Active workout model
class ActiveWorkouts(UserMixin, db.Model):
    workout_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    exercise = db.Column(db.String(100))
    focus = db.Column(db.String(100))
    reps = db.Column(db.Integer)
    complete = db.Column(db.Boolean)
    comments = db.Column(db.String(1000))