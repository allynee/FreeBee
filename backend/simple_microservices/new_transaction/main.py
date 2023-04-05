from flask import Flask, jsonify, request
from database import db
from models import Transaction
import crud


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin1:12345678@esdeeznutspublic.cwjfrbjqz4fp.ap-southeast-1.rds.amazonaws.com:3306/transaction'

@app.route('/transaction', methods=['GET'])
def get_all_transactions():
    transaction_list = crud.get_all()
    if len(transaction_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transaction": [transaction.json() for transaction in transaction_list]
                }
            }
        )
    return jsonify(
        {
        "code": 404,
        "message": "There are no transactions."
        }
    ), 404

if __name__ == '__main__':
    app.run(debug=True)