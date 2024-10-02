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

    if request.method == 'POST':
        # Authenticate User
        username = request.form["username"]   
        entered_password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user is None:
            error_msg = "Username not Found!"
            return render_template("pages/login/login.html", error_msg=error_msg)

        passed = check_password_hash(user.password_hash, entered_password)

        
        # Start User Session
        if passed:
            session.permanent = True
            session["user"] = username
            

            if  referrer == '/affiliate-program/about':
                return redirect(url_for('affiliate.affiliate_signup'))
            else:
                return redirect(url_for('login.user'))
        else:
            error_msg = "Incorrect Password. Try Again."
            return render_template("pages/login/login.html", error_msg=error_msg)
    else:
        referrer = request.referrer
        session['referrer'] = urlparse(referrer).path if referrer else None

        return render_template("pages/login/login.html", error_msg="")

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

        pwd_error = ""
        username_error = ""
        email_error = ""

        if len(password) >= 8:
            pwd_error = "Password must be at least 8 characters long."
            return render_template("pages/login/signup.html", 
                                   pwd_error=pwd_error, 
                                   username_error=username_error,
                                   email_error=email_error)

        referral = request.form['referral'] if request.form['referral'] != '' else None
        
        hashed_pw = generate_password_hash(password)
        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()

        if user_email is None and user_username is None:
            create(db, User, first_name=fname, last_name=lname, username=username, password_hash=hashed_pw, email=email, referral=referral)

            # Create Media Directory
            media_dir = os.path.join(get_root_path(), '..', 'userData', username)
            render_dir = os.path.join(get_root_path(), '..', 'userData', username, 'renders')
            os.mkdir(media_dir)
            os.mkdir(render_dir)

            # Start User Session
            session.permanent = True  
            session["user"] = username
            flash("User added succesfully!")

            return render_template("pages/profile.html", user=username)
        
        elif user_username:
            username_error = "Username already taken"
            return render_template("pages/login/signup.html", 
                                   pwd_error=pwd_error, 
                                   username_error=username_error,
                                   email_error=email_error)
        else:
            email_error = "Email already taken"
            return render_template("pages/login/signup.html", 
                                   pwd_error=pwd_error, 
                                   username_error=username_error,
                                   email_error=email_error)
            

    return render_template("pages/login/signup.html", 
                                   pwd_error=pwd_error, 
                                   username_error=username_error,
                                   email_error=email_error)

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
        