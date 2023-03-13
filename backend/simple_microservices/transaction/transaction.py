from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin1:12345678@esdeeznutspublic.cwjfrbjqz4fp.ap-southeast-1.rds.amazonaws.com:3306/transaction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

sql_file = open('mysql+pymysql://admin1:12345678@esdeeznutspublic.cwjfrbjqz4fp.ap-southeast-1.rds.amazonaws.com:3306/transaction', 'r')


class Transaction(db.Model):
    __tablename__ = 'transaction'


    transaction_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    listing_ID = db.Column(db.Integer, nullable=False)
    user_ID = db.Column(db.Integer, nullable=False)
    corporate_ID = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(13), nullable=False)


    def __init__(self, transaction_ID, listing_ID, user_ID, corporate_ID, status):
        self.transaction_ID = transaction_ID
        self.listing_ID = listing_ID
        self.user_ID = user_ID
        self.corporate_ID = corporate_ID
        self.status = status

    def json(self):
        return {"transaction_ID": self.transaction_ID, "listing_ID": self.listing_ID, "user_ID": self.user_ID, "corporate_ID": self.corporate_ID, "status": self.status}

@app.route("/")
def index():
    return "Hello World"

@app.route("/transaction")
def get_all():
    return jsonify({"transactions": [transaction.json() for transaction in Transaction.query.all()]})

@app.route("/transaction/transaction_ID", methods=["GET"])
def find_by_transactionID(transaction_ID):
    return jsonify(
            {
                "code": 200,
                "data": {
                    "transaction_id":  1,
                    "listing_id": 1,
                    "user_id": 1,
                    "corporate_id": 1,
                    "status": "Completed"
                }
            }, 200
        )

@app.route("/transaction/<int:transaction_ID>", methods=["POST"])
def create_transaction():
    return jsonify(
            {
                "code": 201,
                "data": {
                    "transaction_id":  1,
                    "listing_id": 1,
                    "user_id": 1,
                    "corporate_id": 1,
                    "status": "Completed"
                }
            }, 201
        )

if __name__ == "__main__":
    app.run(port=5000, debug=True)