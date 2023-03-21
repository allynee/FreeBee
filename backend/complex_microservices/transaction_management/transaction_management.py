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

@app.route("/transaction_management", methods=['PUT'])
def update_transaction():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            transaction = request.get_json()
            print("\nReceived an transaction in JSON:", transaction)

            # do the actual work
            # 1. initiate update of transaction
            result = processUpdateTransaction(transaction_)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

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


def processUpdateTransaction(transaction):
    # 2. Send the transaction info {cart items}
    # Invoke the transaction microservice
    print('\n-----Invoking transaction microservice-----')
    transaction_result = invoke_http(transaction_URL, method='PUT', json=transaction)
    print('transaction_result:', transaction_result)

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)