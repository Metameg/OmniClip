from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from app.extensions import db, csrf
from app.tools.database import create
from app.models.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.tools.utilities import get_root_path
import os
from urllib.parse import urlparse

blueprint = Blueprint('login', __name__)

@blueprint.route('/login', methods=['POST', 'GET'])
def login():
    csrf.protect()
    referrer = session.get('referrer', None)
    print("parsed: ", referrer)

    if request.method == 'POST':
        # Authenticate User
        username = request.form["username"]   
        entered_password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user is None:
            print("Username not found!")
            return render_template("pages/login/login.html")

        passed = check_password_hash(user.password_hash, entered_password)

        
        # Start User Session
        if passed:
            session.permanent = True
            session["user"] = username
            

            if  referrer == '/affiliate-program/about':
                print('here')
                return redirect(url_for('affiliate.affiliate_signup'))
            else:
                print('there')
                return redirect(url_for('login.user'))
        else:
            print("Incorrect Password!")
            return render_template("pages/login/login.html")
    else:
        referrer = request.referrer
        session['referrer'] = urlparse(referrer).path if referrer else None
        print("Referrer: " , request.referrer)
        print("Parsed: " , session['referrer'])

        return render_template("pages/login/login.html")

@blueprint.route('/signup', methods=['POST', 'GET'])
def signup():
    if "user" in session:
        return redirect(url_for('login.user'))
    
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        referral = request.form['referral'] if request.form['referral'] != '' else None
        
        hashed_pw = generate_password_hash(password)
        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()

        if user_email is None and user_username is None:
            create(db, User, first_name=fname, last_name=lname, username=username, password_hash=hashed_pw, email=email, referral=referral)

            # Create Media Directory
            media_dir = os.path.join(get_root_path(), '..', 'userData', username)
            os.mkdir(media_dir)

            # Start User Session
            session.permanent = True  
            session["user"] = username
            flash("User added succesfully!")

            return render_template("pages/profile.html", user=username)
        
        elif user_username:
            print("Username already exists!")
            flash("Username already exists!")
        else:
            print("This email is already taken!")
            flash("This email is already taken!")
            

    return render_template("pages/login/signup.html")

@blueprint.route('/profile')
def user():
    if "user" in session:
        username = session["user"]
        return render_template("pages/profile.html", user=username)
    else: 
        return redirect(url_for('login.login'))
    
@blueprint.route('/logout')
def logout():
    session.pop("user", None)
    session.clear()
    return render_template('pages/login/logout.html')
        