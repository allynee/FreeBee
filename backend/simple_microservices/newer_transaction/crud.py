from sqlalchemy.orm import Session
import models
import schemas
from fastapi.encoders import jsonable_encoder
from typing import Dict, Union, Any
import datetime
from fastapi import HTTPException

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).offset(skip).limit(limit).all()

def get_transaction(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.transaction_id == transaction_id).first()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    transaction = models.Transaction(**transaction.dict())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction