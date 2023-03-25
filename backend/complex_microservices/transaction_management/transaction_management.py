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
authentication_URL = "localhost:3001"


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

def processCreateTransaction(transaction, quantityDeducted):

    # 2. Authenticate user
    print('\n-----Authenticating user-----')
    authentication_URL_full = authentication_URL + "/wtf@gmail.com/test1234" #this is currently HARDCODED!!
    authentication_result = invoke_http(authentication_URL_full, method="GET", json=None)
    print('authentication_result:', authentication_result)

    # 3. Create the transaction info
    # Invoke the transaction microservice
    print('\n-----Invoking transaction microservice-----')
    transaction_result = invoke_http(transaction_URL, method='POST', json=transaction)
    print('transaction_result:', transaction_result)
    print('listing_id', transaction_result['listing_id'])

    listing_id = transaction_result['listing_id'] #get listing_id of newly created transaction

    #4. Update listing quantity

    #Get existing listing details
    print('\n-----Invoking listing management microservice-----')
    listing_result = invoke_http(transaction_URL, method='GET', json=None)
    print('listing_result:', listing_result)


    #Create listing json object

    # Invoke listing management
    print('\n-----Invoking listing management microservice-----')
    listing_result = invoke_http(transaction_URL, method='PUT', json=)





if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing a transaction...")
    app.run(host="0.0.0.0", port=5100, debug=True)