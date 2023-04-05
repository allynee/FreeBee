from models import Transaction
from database import db
from flask import jsonify, request

# def create_transaction(amount):
#     transaction = Transaction(amount=amount)
#     db.session.add(transaction)
#     db.session.commit()
#     return transaction

def get_all():
    # transaction_list = Transaction.query.all()
    return jsonify({"transactions": [transaction.json() for transaction in Transaction.query.all()]})

# @app.route("/transaction", methods=["POST"])
# def create_transaction():
#     data = request.get_json()
#     transaction = Transaction(**data)

#     if Transaction.query.filter_by(listing_id=transaction.listing_id, user_id=transaction.user_id).first():
#         return jsonify(
#             {
#                 "code": 400,
#                 "data": {
#                     "transaction_ID": transaction_id
#                 },
#                 "message": "A transaction with listing ID '{}' and user ID '{}' already exists.".format(transaction.listing_id, transaction.user_id)
#             }
#         ), 400
#     try:
#         db.session.add(transaction)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "transaction_ID": transaction_id
#                 },
#                 "message": "An error occurred creating the transaction."
#             }
#         ), 500
    
#     return jsonify(transaction)