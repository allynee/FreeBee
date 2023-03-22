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
listing_URL = "http://localhost:8000/listing"

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

@app.route("/listing_update", methods=['PUT'])
def update_listing(listing):
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            listing = request.get_json()
            print("\nUpdated listing in JSON:", listing)

            # do the actual work
            # 1. initiate creation of listing
            result = processUpdateListing(listing)
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

def processCreateTransaction(transaction):
    # 2. Send the transaction info
    # Invoke the transaction microservice
    print('\n-----Invoking transaction microservice-----')
    transaction_result = invoke_http(transaction_URL, method='POST', json=transaction)
    print('transaction_result:', transaction_result)

def processUpdateListing(listing):
    # 2. Send the listing info
    # Invoke the listing microservice
    print('\n-----Invoking listing microservice-----')
    listing_result = invoke_http(listing_URL, method='PUT', json=listing)
    print('listing_result:', listing_result)    


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing a transaction...")
    app.run(host="0.0.0.0", port=5100, debug=True)