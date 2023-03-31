# To run with debug: uvicorn main:app --reload --host 0.0.0.0 --port 9000

'''
Here core functions are defined for different operations.
'''

from typing import Dict, List
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal, engine
import models
import schemas
import crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
Insert relavant operations below
'''

### TEST ###
@app.get('/ping')
def ping():
    return 'pong'

### GET ALL TRANSACTIONS ###
@app.get('/transaction', response_model=List[schemas.Transaction])
def get_all_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db,skip=skip,limit=limit)
    if transactions is None:
        raise HTTPException(status_code=404, detail="No transactions available")
    return transactions

### GET TRANSACTIONS BASED ON BENEFICIARY ID ###
@app.get('/transaction/beneficiary/{beneficiary_id}', response_model=List[schemas.Transaction])
def get_transactions_by_beneficiary(beneficiary_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100,):
    transaction = crud.get_transactions_by_beneficiary(db, beneficiary_id=beneficiary_id, skip=skip,limit=limit)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Beneficiary has no transactions")
    return transaction

### GET TRANSACTIONS BASED ON CORPORATE ID ###
@app.get('/transaction/corporate/{corporate_id}', response_model=List[schemas.Transaction])
def get_transactions_by_corporate(corporate_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100,):
    transaction = crud.get_transactions_by_corporate(db, corporate_id=corporate_id, skip=skip,limit=limit)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Corporate has no transactions")
    return transaction

# ### GET SINGLE TRANSACTION BASED ON TRANSACTION ID ###
@app.get('/transaction/{transaction_id}', response_model=schemas.Transaction)
def get_transaction_by_id(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.get_transaction(db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
    
### CREATE SINGLE TRANSACTION ###
@app.post('/transaction', response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db=db, transaction=transaction)

### UPDATE ANY FIELD IN TRANSACTION ###
@app.put('/transaction/{transaction_id}', response_model=schemas.Transaction)
def update_transaction(transaction_id: int, transaction: schemas.TransactionUpdate, db: Session = Depends(get_db)):
    return crud.update_transaction(db, transaction_id=transaction_id, data=transaction)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=9000)