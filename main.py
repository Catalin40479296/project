from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import date
from init import db
from init import app

from models import ActiveWorkouts

main = Blueprint('main', __name__)


#index page, rendering active workouts and giving date, workouts found on the user id and the name of the use
@main.route('/')
def index():
     return render_template('login.html')

@main.route('/active-workouts')
@login_required
def active_workouts():
    current_workouts = ActiveWorkouts.query.filter_by(username = current_user.name)

    today = date.today()
    return render_template('active-workouts.html', today = today.strftime("%d/%m/%y"), current_workouts = current_workouts, name = current_user.name)

#add workout route
@main.route('/add-workout', methods=["POST"])
def add_workout():
    exercise = request.form.get("exercise")
    focus = request.form.get("focus")
    reps = request.form.get("reps")
    new_workout = ActiveWorkouts(username=current_user.name, exercise=exercise, focus = focus, reps = reps, complete=False)
    db.session.add(new_workout)
    db.session.commit()
    return redirect(url_for("main.active_workouts"))

#delete workout route
@main.route('/delete/<int:workout_id>')
def delete(workout_id):
    workout = ActiveWorkouts.query.filter_by(workout_id = workout_id).first()
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for("main.active_workouts"))

#update route with method POST
@main.route('/update/<int:workout_id>', methods=["POST"])
def update(workout_id):
    updated_workout = ActiveWorkouts.query.filter_by(workout_id = workout_id).first()
    updated_workout.exercise = request.form.get("exercise")
    updated_workout.focus = request.form.get("focus")
    updated_workout.reps = request.form.get("reps")
    db.session.commit()
    return redirect(url_for("main.active_workouts"))

#update route with method GET, showing the form 
@main.route('/update/<int:workout_id>', methods=["GET"])
def changed(workout_id):
    changed_workout = ActiveWorkouts.query.filter_by(workout_id = workout_id).first()
    return render_template("update-workout.html", changed_workout = changed_workout)

#completed route, changing the completed boolean value
@main.route('/completed/<int:workout_id>')
def complete(workout_id):
    done_workout = ActiveWorkouts.query.filter_by(workout_id = workout_id).first()
    done_workout.complete = not done_workout.complete
    db.session.commit()
    return redirect(url_for("main.active_workouts", done_workout = done_workout.complete))

#comments route, method POST to save the comment to the database
@main.route('/comments/<int:workout_id>', methods=["POST"])
def comments(workout_id):
    comment_workout = ActiveWorkouts.query.filter_by(workout_id = workout_id).first()
    comment_workout.comments = request.form.get("comments")
    db.session.commit()
    return redirect(url_for("main.active_workouts"))

#comments route, method GET to show the form and the current comment if any
@main.route('/comments/<int:workout_id>', methods=["GET"])
def comments_get(workout_id):
    comment_workout = ActiveWorkouts.query.filter_by(workout_id = workout_id).first()
    return render_template("add-comments.html", comment_workout = comment_workout)


#workout page
@main.route('/workouts')
def workouts():
    return render_template('workouts.html')

