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
    
    user = database.retrieve(User, username=username)
    if user.subscription_id != 0:
        return redirect(url_for('general.login_subscription', username=username, selected_pill='subscription'))
    
    
    if package == 'pro':
        price = 15.99
        plan_id = 'P-4Y884424610529704MYP7XJQ'
    if package == 'enterprise':
        price = 24.99

    # access_token = create_access_token(identity=username)
    # print(access_token)
    # response = make_response(render_template("pages/checkout.html", package=package, price=price))
    # set_access_cookies(response, access_token)
    link_paypal_subscription_url = 'http://127.0.0.1:5000/payments/link-paypal-subscription'
    return render_template("pages/checkout.html", package=package, price=price, plan_id=plan_id, link_paypal_subscription_url=link_paypal_subscription_url)