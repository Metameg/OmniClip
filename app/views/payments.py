from flask import Blueprint, request, jsonify, session, redirect, url_for
from app.tools import helpers, database
from app.models.User import  User
from app.models.Media import  Media
from app.extensions import db, csrf
import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth
from flask_jwt_extended import jwt_required
import os
import json
from dotenv import load_dotenv

 #FIXME Replace this for production ->  "https://api-m.paypal.com"
PAYPAL_ORDER_BASE_URL = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
PAYPAL_SUBSCRIPTION_BASE_URL = "https://api-m.sandbox.paypal.com/v1/billing/subscriptions"






def create_order(
    *,
    value_usd: str,
) -> dict:
    """Create a PayPal order."""

    headers = construct_paypal_auth_headers()

    response = requests.post(
       
        url=PAYPAL_ORDER_BASE_URL,
        headers=headers,
        json={
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": value_usd,
                    },
                },
            ],
        },
    )
    try:
        response.raise_for_status()
    except HTTPError as error:
        print(error)

    return response.json()


def capture_order(
    *,
    paypal_order_id: str,
) -> dict:
    headers = construct_paypal_auth_headers()

    response = requests.post(
        url=f"{PAYPAL_ORDER_BASE_URL}/{paypal_order_id}/capture",
        headers=headers,
        # Uncomment one of these to force an error for negative testing
        # (in sandbox mode only).
        # Documentation:
        # https://developer.paypal.com/tools/sandbox/negative-testing/request-headers/
        # "PayPal-Mock-Response": '{"mock_application_codes": "INSTRUMENT_DECLINED"}'
        # "PayPal-Mock-Response": '{"mock_application_codes": "TRANSACTION_REFUSED"}'
        # "PayPal-Mock-Response": '{"mock_application_codes": "INTERNAL_SERVER_ERROR"}'
    )

    try:
        response.raise_for_status()
    except HTTPError as error:
        print(error)

    return response.json()




def get_auth_token() -> str:
    """Get an auth token from PayPal."""
    
    load_dotenv()
    client_id = os.getenv('PAYPAL_CLIENT_ID')
    paypal_secret = os.getenv('PAYPAL_SECRET')

    response = requests.post(
        url="https://api-m.sandbox.paypal.com/v1/oauth2/token",
        auth=(
            client_id,  # type: ignore
            paypal_secret,  # type: ignore
        ),  # type: ignore
        data={
            "grant_type": "client_credentials",
        },
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)

    return response.json()["access_token"]


def construct_paypal_auth_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {get_auth_token()}",
        "Content-Type": "application/json",
    }


def get_subscription(
    *,
    paypal_subscription_id: str,
) -> dict:
    headers = construct_paypal_auth_headers()

    response = requests.get(
        url=f"{PAYPAL_SUBSCRIPTION_BASE_URL}/{paypal_subscription_id}",
        headers=headers,
    )

    try:
        response.raise_for_status()
    except HTTPError as error:
        print(error)

    return response.json()


def subscription_is_active(
    *,
    paypal_subscription_id: str,
) -> bool:
    """Check the status of a PayPal subscription."""
    # Check the cache first
    cache_key = f"paypal_subscription_{paypal_subscription_id}"
    # status = cache.get(cache_key)

    # if status is None:
    try:
        subscription = get_subscription(
            paypal_subscription_id=paypal_subscription_id,
        )
    except Exception as e:
        print(e)
        return False

    status = subscription["status"]

        # Cache the status for one day
        # cache.set(
        #     cache_key,
        #     status,
        #     60 * 60 * 24,  # 24 hours
        # )

    return status == "ACTIVE"



# load_dotenv()
# paypal_secret = os.getenv('PAYPAL_SECRET')

# blueprint = Blueprint('payments', __name__)
# csrf.exempt(blueprint)

# @blueprint.route('<package>/<order_id>/capture', methods=['POST'])
# # @jwt_required()
# def capture_payment(package, order_id):  # Checks and confirms payment
#     print("processing payment")
#     # csrf.protect()
#     captured_payment = approve_payment(package, order_id)
#     # print(captured_payment) # or you can do some checks from this captured data details
#     return jsonify(captured_payment)


# # JWT-protected route
# @blueprint.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     # Access token is valid
#     # return jsonify({'message': 'You have access to this route'}), 200
#     return redirect(url_for('thank_you'))

# # Thank you page (also protected by JWT)
# @blueprint.route('/thank_you')
# @jwt_required()
# def thank_you():
#     return '<h1>Thank you for your payment!</h1>'

# def approve_payment(package, order_id):
#     pro_price = "15.99"
#     enterprise_price = "24.99"
#     api_link = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
#     client_id = "AeKSoG7ueATSYqBRKyWYBy5r6NxmNWbORH1ruWttBRuBuXUsOs11pEitl_doWfJn00ynN3BHrelHg6Sr"
#     basic_auth = HTTPBasicAuth(client_id, paypal_secret)
#     headers = {
#         "Content-Type": "application/json",
#     }
#     response = requests.post(url=api_link, headers=headers, auth=basic_auth)
#     response.raise_for_status()

#     json_data = response.json()
#     # Verify correct price 
#     received_price = json_data['purchase_units'][0]['payments']['captures'][0]['amount']['value']
#     correct_amount = (package == 'pro' and  received_price == pro_price) \
#                      or (package == 'enterprise' and received_price == enterprise_price)
        
#     print(json.dumps(json_data, indent=4))
#     if json_data['status'] == 'COMPLETED' and json_data['payment_source']['paypal']['account_status'] == 'VERIFIED':
#         if correct_amount:
#             print("correct amount paid: ", received_price)
#             msg = "Payment Successful!"
#             # return redirect(url_for('subscriptions.checkout', package=package, msg=msg))
#             return json_data
#         else:
#             msg = "Unable to process payment. Please try again."
#             return json_data
#             # return redirect(url_for('subscriptions.checkout', package=package, msg=msg))


#     # return json_data