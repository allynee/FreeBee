from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

transaction_URL = environ.get('transaction_URL') or "http://localhost:9000/transaction"
listing_URL = environ.get('listing_URL') or "http://localhost:8000/listing"
authentication_URL = environ.get('auth_URL') or "http://localhost:3001/auth/checkaccess/"

@app.route("/transaction_management", methods=['POST'])
def create_transaction():
        # Simple check of input format and data of the request are JSON
        if request.is_json:
            try:
                required_details = request.get_json()
                print("\nJSON to create transaction:", required_details)
                # do the actual work
                # 1. initiate creation of transaction
                listing = required_details["listing"]
                beneficiary_id = required_details["beneficiary_id"]
                quantityDeducted = required_details["quantity"]
                token = required_details["token"]
                result = processCreateTransaction(listing, beneficiary_id, quantityDeducted, token)
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


@app.route("/transaction_management", methods=['PUT']) #assuming i get transaction and listing
def update_transaction():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            required_details = request.get_json()
            print("\nJSON with details to update in transaction:", required_details)
            listing = required_details["listing"]
            transactions = required_details["transactions"]
            token = required_details["token"]
            status = required_details["status"]
            # do the actual work
            # 1. initiate update of transaction
            result = processUpdateTransaction(transactions, listing, token, status)
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

@app.route("/transaction_management/beneficiary/<string:beneficiary_id>", methods=["GET"])
def view_transactions_beneficiary(beneficiary_id):

    results = []

    #1. Retrieve transactions associated with beneficiary  
    print('\n-----Retrieving transactions-----')
    transaction_URL_full = transaction_URL + f"/beneficiary/{beneficiary_id}"
    transaction_result = invoke_http(transaction_URL_full, method="GET", json=None)
    print('transaction_result:', transaction_result)

    if transaction_result["code"] == 200 and len(transaction_result["result"]) > 0:

        for transaction in transaction_result["result"]:
            listing_id = transaction["listing_id"]
            print('\n-----Retrieving listing details for each transaction-----')
            listing_URL_full = listing_URL + f"/{listing_id}"
            listing_result = invoke_http(listing_URL_full, method="GET", json=None)
            print('listing_result:', listing_result)

            if listing_result["code"] == 200:
                transaction["listing_details"] = listing_result["result"]
                print('\n-----Retrieving image details for listing-----')
                img_ext = listing_result["result"]["img_ext"]
                firebase_url = f"https://firebasestorage.googleapis.com/v0/b/esdeeznutz.appspot.com/o/listings%2F{listing_id}{img_ext}?alt=media&token=d96a1b6f-e4a2-42d1-a06b-c9331d4490a4"
                transaction["image_url"] = firebase_url
            print('\nEdited transaction:', transaction)
            results.append(transaction)
    else:
        return {
            "code": transaction_result["code"],
            "message": "Unable to return transactions"
        }

    return {
        "code": 200,
        "message": "Retrieving transactions via beneficiary_id was successful",
        "result":  results
    }

@app.route("/transaction_management/corporate/<string:listing_id>", methods=["GET"]) #for corporate view of transactions associated with listings
def view_transactions_corp(listing_id):

    #1. Retrieve transactions associated with corporate's listing 
    print('\n-----Retrieving transactions-----')
    transaction_URL_full = transaction_URL + f"/listing/{listing_id}"
    transaction_result = invoke_http(transaction_URL_full, method="GET", json=None)
    print('transaction_result:', transaction_result)

    #2. Retrieve listing details

    listing_URL_full = listing_URL + f"/{listing_id}"
    listing_result = invoke_http(listing_URL_full, method="GET", json=None)
    
    results = {"transactions": transaction_result, 'listing_details': listing_result}
    return {
        "code": 200,
        "message": "Retrieving transactions via corporate_id was successful",
        "result":  results
    }

def processCreateTransaction(listing, beneficiary_id, quantityDeducted, token):
    listing_id = listing["listing_id"]
    corporate_id = listing["corporate_id"]

    # 2. Authenticate user
    authentication_result = authenticateUser(token) 
    if authentication_result["statusCode"] == '200':
        if (authentication_result['role'] == "beneficiary"):
            
            # 3. Create the transaction info
            transaction = {
                "listing_id": listing_id,
                "corporate_id": corporate_id,
                "beneficiary_id": beneficiary_id,
                "status": "In Progress",
                "quantity": int(quantityDeducted)
            }
            #4. Check that beneficiary can deduct quantity requested from listing
            #4a. Get existing listing details
            existing_quantity = int(listing["quantity"])
            #4b. Deduct quantity from  listing
            new_quantity = existing_quantity - int(quantityDeducted)
            new_listing = {"quantity": new_quantity}
            if new_quantity >= 0: #if sufficient quantity
                print('\n-----Updating listing-----')
                listing_URL_full = listing_URL + "/" + str(listing_id)
                listing_result = invoke_http(listing_URL_full, method='PUT', json=new_listing) 
                print('listing_result:', listing_result)
                if listing_result["code"] != 200: #terminate process
                    return {
                        "code": listing_result["code"],
                        "message": "Listing not found or listing update was not successful. View error code for more info."
                    }, listing_result["code"]
            else: #terminate process
                return{
                    "code": 500,
                    "message": "Insufficient quantity to claim."
                }, 500

            # 5. If quantity has depleted to 0, send AMQP to corporate
            if new_quantity == 0:
                amqp_listing_msg = listing
                amqp_listing_msg['quantity'] = 0
                print("\n------------------Sending AMQP for no more qty to corporate------------------")
                obj = {
                    "purpose": "toCorporate",
                    "listing_result": amqp_listing_msg
                }
                message = json.dumps(obj)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="corporate.notif", 
                    body=message, properties=pika.BasicProperties(delivery_mode = 2))
                print(f"sending message: {message} to 'notify corporate'")
                
                # 5a. Change listing status to unavailable
                listing_URL_full = listing_URL + "/" + str(listing_id)
                listing_update = {"status": "Unavailable"}
                listing_result = invoke_http(listing_URL_full, method='PUT', json=listing_update)
                print('listing_result:', listing_result)
                if listing_result["code"] != 200:
                    return {
                        "code": listing_result["code"],
                        "message": "Listing not found or listing update was not successful. View error code for more info."
                    }, listing_result["code"]

            # 6. Invoke the transaction microservice
            print('\n-----Invoking transaction microservice-----')
            transaction_result = invoke_http(transaction_URL, method='POST', json=transaction)
            print('transaction_result:', transaction_result)
            if transaction_result["code"] != 200:
                return {
                    "code": transaction_result["code"],
                    "message": "Transaction creation not successful."
                }, transaction_result["code"]
            
            print("------------------Sending AMQP for successful claim to beneficiary------------------")
            # 7. Notify beneficiaries that claim has been successful
            if transaction_result["result"]["status"] == "In Progress":
                obj = {
                    "purpose": "toBeneficiary",
                    "listing_result": listing,
                    "transaction_result": transaction
                }
                message = json.dumps(obj)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="change.notif", 
                    body=message, properties=pika.BasicProperties(delivery_mode = 2))
                print(f"sending message: {message} to 'claim successful'")

            return {
                "code": 200,
                "message": "Congrats transaction claim successful"
            }, 200
    else:
        return {
            "code": 404,
            "message": "Unauthenticated user. User needs to be logged into a beneficiary account."
        }, 404

def processUpdateTransaction(transactions, listing, token, status):

    listing_id = listing["listing_id"]

    #2. Authenticate user
    authentication_result = authenticateUser(token)
    return_listing = []
    if authentication_result["statusCode"] == "200":
        for transaction in transactions:
            transaction_id = transaction["transaction_id"]
            #3. Update transaction
            transaction_URL_full = transaction_URL + "/" + str(transaction_id)
            print('\n-----Invoking transaction microservice-----')
            transaction_update = {
                "status": status
            }
            transaction_result = invoke_http(transaction_URL_full, method='PUT', json=transaction_update)
            print('transaction_results:', transaction_result)    

        #4. Notify users if theres is a change in the status of the transaction

        #4a. If transaction is Cancelled from Corporate
        # CHANGED transaction_result['status'] to status because AMQP was recieving the outdated status
            if status == "Cancelled":
                print('\n-----Send to Notification microservice-----')
                obj = {
                    "purpose": "cancelled",
                    "listing_result": listing
                } 
                message = json.dumps(obj)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="cancel.notif", 
                    body=message, properties=pika.BasicProperties(delivery_mode = 2))
                print(f"sending message: {message} to 'cancel'")
                #4b. update listing to unavailable
                listing_URL_full = listing_URL + "/" + str(listing_id)
                listing_update = {"status": "Unavailable"}
                listing_result = invoke_http(listing_URL_full, method='PUT', json=listing_update)
                print('listing_result:', listing_result)
                return_listing.append({"code": 200, "message": "Transaction status successfully updated, cancelled."})

            #4c. If items are Ready to Collect or Completed
            elif status == "Ready for Collection" or "Completed":
                obj = {
                    "purpose": "toBeneficiary",
                    "listing_result": listing,
                    "transaction_result": transaction
                }
                message = json.dumps(obj)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="change.notif", 
                    body=message, properties=pika.BasicProperties(delivery_mode = 2))
                print(f"sending message: {message} to 'collect'")
                return_listing.append({"code": 200 ,"message": f"Success transaction status changed to {status}"})
            
            else:
                return {"code": 500, "message": "Invalid status."}
        return {"code": 200, "result": return_listing}  

def authenticateUser(token_input):
    print('\n-----Authenticating user-----')
    authentication_URL_full = authentication_URL + token_input #need to get token from the front-end, currently HARDCODED
    authentication_result = invoke_http(authentication_URL_full, method="GET", json=None)
    print('authentication_result:', authentication_result)
    return authentication_result["result"]

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing a transaction...")
    app.run(host="0.0.0.0", port=5100, debug=True)