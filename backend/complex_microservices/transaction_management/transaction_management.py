from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

# import amqp_setup
# import pika
# import json

app = Flask(__name__)
CORS(app)

transaction_URL = "http://localhost:9000/transaction"
listing_management_URL = "http://localhost:5000/listing_management"
authentication_URL = "localhost:3001/"

transaction_status = "Ready to Collect"

@app.route("/transaction_management", methods=['POST'])
def create_transaction():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            transaction = request.get_json()
            print("\nCreated a transaction in JSON:", transaction)

            # do the actual work
            # 1. initiate creation of transaction
            result = processCreateTransaction(transaction)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "create_transaction.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


@app.route("/transaction_management/<int:transaction_id>", methods=['PUT'])
def update_transaction(transaction_id):
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            transaction = request.get_json()
            print("\nJSON with details to update in transaction:", transaction)

            # do the actual work
            # 1. initiate update of transaction
            result = processUpdateTransaction(transaction, transaction_id)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "transaction service internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processCreateTransaction(transaction, quantityDeducted):
    # 2. Authenticate user
    print('\n-----Authenticating user-----')
    authentication_URL_full = authentication_URL + "auth/checkaccess/:token" #need to get token from the front-end
    authentication_result = invoke_http(authentication_URL_full, method="GET", json=None)
    print('authentication_result:', authentication_result)

    if authentication_result["statusCode"] == 200:

        # 3. Create the transaction info
        # Invoke the transaction microservice
        print('\n-----Invoking transaction microservice-----')
        transaction_result = invoke_http(transaction_URL, method='POST', json=transaction)
        print('transaction_result:', transaction_result)
        print('listing_id', transaction_result['listing_id'])

        listing_id = transaction_result['listing_id'] #get listing_id of newly created transaction

        #4. Update listing quantity
        print('\n-----Invoking listing management microservice-----')
        #4a. Get existing listing details
        listing_management_URL_full = listing_management_URL + "/" + str(listing_id)
        listing_result = invoke_http(listing_management_URL_full, method='GET', json=None)
        print('listing_result:', listing_result)
        existing_quantity = listing_result["quantity"]
        #4b. Deduct quantity from  listing
        new_quantity = existing_quantity - quantityDeducted
        new_listing = {"quantity": new_quantity}
        if new_quantity >= 0:
            listing_result = invoke_http(listing_management_URL_full, method='PUT', json=new_listing)  

def processUpdateTransaction(transaction, transaction_id):

    #2. Authenticate user
    #copy code from above. set conditional statement of code == 200

    #3. Update transaction
    transaction_URL_full = transaction_URL + "/" + str(transaction_id)
    print('\n-----Invoking transaction microservice-----')
    transaction_result = invoke_http(transaction_URL_full, method='PUT', json=transaction)
    print('transaction_result:', transaction_result)    

    #4. Notify users if theres is a change in the status of the transaction

    #4a. If transaction is Cancelled from Corporate
    if transaction_result["status"] == "Cancelled":
        pass #notify beneficiaries

    #4b. If transaction is Cancelled from Beneficiary
    if transaction_result["status"] == "Cancelled":
        pass #notify corporates

    #4c. If items are Ready to Collect
    if transaction_result["status"] == "Ready to Collect":
        pass #notify beneficiaries

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing a transaction...")
    app.run(host="0.0.0.0", port=5100, debug=True)