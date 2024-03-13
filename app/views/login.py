from flask import Blueprint, render_template, request, url_for, redirect, session
from app import db, csrf

blueprint = Blueprint('login', __name__)

@blueprint.route('/login', methods=['POST', 'GET'])

def login():
    csrf.protect()
    if request.method == 'POST':
        session.permanent = True
        user = request.form["username"]   
        session["user"] = user
        return redirect(url_for('login.user'))
    else:
        return render_template("pages/login/login.html")

@blueprint.route('/sign-up')
def signup():
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
        