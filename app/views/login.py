from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from app.extensions import db, csrf
# from app import csrf
from app.models.User import User
from werkzeug.security import generate_password_hash

blueprint = Blueprint('login', __name__)

@blueprint.route('/login', methods=['POST', 'GET'])
def login():
    csrf.protect()
    if request.method == 'POST':
        # Authenticate User

        # Start User Session
        session.permanent = True
        user = request.form["username"]   
        session["user"] = user
        return redirect(url_for('login.user'))
    else:
        return render_template("pages/login/login.html")

@blueprint.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        hashed_pw = generate_password_hash(password)
        user = User.query.filter_by(username=username).first()

        if user is None:
            new_user = User(first_name=fname,
                        last_name=lname,
                        username=username, 
                        password_hash=hashed_pw,
                        email=email)
            db.session.add(new_user)
            db.session.commit()
            flash("User added succesfully!")
            return render_template("pages/profile.html", user=username)
        
        else:
            flash("Username already exists!")
            

    return render_template("pages/login/signup.html")

@blueprint.route('/profile')
def user():
    if "user" in session:
        user = session["user"]
        return render_template("pages/profile.html", user=user)
    else: 
        return redirect(url_for('login.login'))
    
@blueprint.route('/logout')
def logout():
    session.pop("user", None)
    return render_template('pages/login/logout.html')
        