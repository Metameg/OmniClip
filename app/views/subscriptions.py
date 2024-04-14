from flask import Blueprint, render_template, make_response, session, redirect, url_for, request
from app.tools import database
from app.models.User import  User
from app.extensions import db
from flask_jwt_extended import create_access_token

blueprint = Blueprint('subscriptions', __name__)

@blueprint.route('/pricing')
def pricing():
    return render_template("pages/pricing.html")

@blueprint.route('/checkout/<string:package>')
def checkout(package):
    if "user" not in session:
        return redirect(url_for('login.login'))
    
    username = session["user"]
    # user = database.retrieve(User, username=username)

    #     print(user.subscription_id)
    #     user.subscription_id = 1
    # if package == 'enterprise':
    #     user.subscription_id = 2

    # try:
    #     db.session.commit()
    #     print("User subscription_id added!")
    # except SQLAlchemyError as e:
    #     db.session.rollback()
    #     print("Unable to update user!", e)
    if package == 'pro':
        price = 15.99
    if package == 'enterprise':
        price = 24.99

    access_token = create_access_token(identity=username)
    print(access_token)
    # response = make_response(render_template("pages/checkout.html", package=package, price=price))
    # set_access_cookies(response, access_token)

    return render_template("pages/checkout.html", package=package, price=price, access_token=access_token)