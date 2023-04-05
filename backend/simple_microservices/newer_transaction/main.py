# To run with debug: uvicorn main:app --reload --host 0.0.0.0 --port 8000

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

### GET ALL LISTINGS ###
# @app.get('/transaction', response_model=List[schemas.Listing])
# def get_all_listings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_listings(db,skip=skip,limit=limit)
#     if items is None:
#         raise HTTPException(status_code=404, detail="No listings available")
#     return items

# ### GET SINGLE LISTING BASED ON LISTING ID ###
# @app.get('/listing/{listing_id}', response_model=schemas.Listing)
# def get_listing_by_id(listing_id: int, db: Session = Depends(get_db)):
#     listing = crud.get_listing(db, listing_id=listing_id)
#     if listing is None:
#         raise HTTPException(status_code=404, detail="Listing not found")
#     return listing
    
### CREATE SINGLE LISTING ###
@app.post('/transaction', response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, transaction=transaction)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)