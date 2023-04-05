from database import db

class Transaction(db.Model):
    __tablename__ = 'transaction'


    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    listing_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    corporate_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(13), nullable=False)


    # def __init__(self, transaction_id, listing_id, user_id, corporate_id, status):
    #     self.transaction_id = transaction_id
    #     self.listing_id = listing_id
    #     self.user_id = user_id
    #     self.corporate_id = corporate_id
    #     self.status = status

    def json(self):
        return {"transaction_id": self.transaction_id, "listing_id": self.listing_id, "user_id": self.user_id, "corporate_id": self.corporate_id, "status": self.status}