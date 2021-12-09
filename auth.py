from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from __init__ import db

auth = Blueprint('auth', __name__)

#login route to render the login page
@auth.route('/login')
def login():
    return render_template('login.html')
#login route to receive the data and check it against the database
@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    #check if the email is in the database already
    user = User.query.filter_by(email=email).first()
    
    #check the user and password against the hashed password from the database and redirect if not correct
    if not user and not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    
    #login if correct and redirect to index page
    login_user(user, remember=remember)
    return redirect(url_for('main.active_workouts'))
#signup route that render the signup template
@auth.route('/signup')
def signup():
    return render_template('signup.html')
#signup route that receive the data through POST
@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    #check if user exist by checking the email
    user = User.query.filter_by(email=email).first()

    #redirect and flash message that user exists
    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    #if it does not exist, save the data and commit it to the database, redirecting to the login page
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))
#logout and redirect
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))