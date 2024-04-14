from flask import Blueprint, request, jsonify, session, redirect, url_for
from app.tools import helpers, database
from app.models.User import  User
from app.models.Media import  Media
from app.extensions import db, csrf
import requests
from requests.auth import HTTPBasicAuth
# from flask_jwt_extended import jwt_required
import os
import json
from dotenv import load_dotenv



load_dotenv()
paypal_secret = os.getenv('PAYPAL_SECRET')

blueprint = Blueprint('payments', __name__)
csrf.exempt(blueprint)

@blueprint.route('<package>/<order_id>/capture', methods=['POST'])
# @jwt_required()
def capture_payment(package, order_id):  # Checks and confirms payment
    print("processing payment")
    # csrf.protect()
    captured_payment = approve_payment(package, order_id)
    # print(captured_payment) # or you can do some checks from this captured data details
    return jsonify(captured_payment)

def approve_payment(package, order_id):
    pro_price = "15.99"
    enterprise_price = "24.99"
    api_link = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
    client_id = "AeKSoG7ueATSYqBRKyWYBy5r6NxmNWbORH1ruWttBRuBuXUsOs11pEitl_doWfJn00ynN3BHrelHg6Sr"
    basic_auth = HTTPBasicAuth(client_id, paypal_secret)
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url=api_link, headers=headers, auth=basic_auth)
    response.raise_for_status()

    json_data = response.json()
    # Verify correct price 
    received_price = json_data['purchase_units'][0]['payments']['captures'][0]['amount']['value']
    correct_amount = (package == 'pro' and  received_price == pro_price) \
                     or (package == 'enterprise' and received_price == enterprise_price)
        
    print(json.dumps(json_data, indent=4))
    if json_data['status'] == 'COMPLETED' and json_data['payment_source']['paypal']['account_status'] == 'VERIFIED':
        if correct_amount:
            print("correct amount paid: ", received_price)
            msg = "Payment Successful!"
            # return redirect(url_for('subscriptions.checkout', package=package, msg=msg))
            return json_data
        else:
            msg = "Unable to process payment. Please try again."
            return json_data
            # return redirect(url_for('subscriptions.checkout', package=package, msg=msg))


    return json_data