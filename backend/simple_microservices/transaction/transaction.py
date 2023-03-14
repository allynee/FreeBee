from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin1:12345678@esdeeznutspublic.cwjfrbjqz4fp.ap-southeast-1.rds.amazonaws.com:3306/transaction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

class Transaction(db.Model):
    __tablename__ = 'transaction'


    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    listing_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    corporate_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(13), nullable=False)


    def __init__(self, transaction_id, listing_id, user_id, corporate_id, status):
        self.transaction_id = transaction_id
        self.listing_id = listing_id
        self.user_id = user_id
        self.corporate_id = corporate_id
        self.status = status

    def json(self):
        return {"transaction_id": self.transaction_id, "listing_id": self.listing_id, "user_id": self.user_id, "corporate_id": self.corporate_id, "status": self.status}

@app.route("/")
def index():
    return "Hello World"

@app.route("/transaction")
def get_all():
    transaction_list = Transaction.query.all()
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

@app.route("/transaction/<int:transaction_id>", methods=["GET"])
def find_by_transactionID(transaction_id):
    print("test")
    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if transaction:
        return jsonify(
            {
                "code": 200,
                "data": transaction.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Transaction not found."
        }
    ), 404

@app.route("/transaction", methods=["POST"])
def create_transaction():
    data = request.get_json()
    transaction = Transaction(**data)

    if Transaction.query.filter_by(listing_id=transaction.listing_id, user_id=transaction.user_id).first():
        return jsonify(
            {
                "code": 400,
                "data": {
                    "transaction_ID": transaction_id
                },
                "message": "A transaction with listing ID '{}' and user ID '{}' already exists.".format(transaction.listing_id, transaction.user_id)
            }
        ), 400
    try:
        db.session.add(transaction)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "transaction_ID": transaction_id
                },
                "message": "An error occurred creating the transaction."
            }
        ), 500
    
    return jsonify(transaction)

if __name__ == "__main__":
    app.run(port=5000, debug=True)