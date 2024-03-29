# To run with debug: uvicorn main:app --reload --host 0.0.0.0 --port 8421

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

### CREATION ###

### CREATE SINGLE BENEFICIARY ###
@app.post('/beneficiary', response_model=schemas.Beneficiary)
def create_beneficiary(beneficiary: schemas.BeneficiaryCreate, db: Session = Depends(get_db)):
    return crud.create_beneficiary(db, beneficiary=beneficiary)

### CREATE SINGLE CORPORATE ###
@app.post('/corporate', response_model=schemas.Corporate)
def create_corporate(corporate: schemas.CorporateCreate, db: Session = Depends(get_db)):
    return crud.create_corporate(db, corporate=corporate)

### CREATE SINGLE SUBSCRIPTION ###
@app.post('/subscription', response_model=schemas.Subscription, status_code=201)
def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    return crud.create_subscription(db, subscription=subscription)
### CREATE SINGLE FAVOURITE ###
@app.post('/favourite', response_model=schemas.Favourite, status_code=201)
def create_favourite(favourite: schemas.FavouriteCreate, db: Session = Depends(get_db)):
    return crud.create_favourite(db, favourite=favourite)

### GET STUFF!!! ###

### GET ALL CORPORATES ###
@app.get('/corporate', response_model=List[schemas.Corporate])
def get_all_corporates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    corporates = crud.get_all_corporates(db,skip=skip,limit=limit)
    if corporates is None:
        raise HTTPException(status_code=404, detail="There are no corporates.")
    return corporates

### GET CORPORATE BASED ON CORPORATE ID ###
@app.get('/corporate/{corporate_id}', response_model=schemas.Corporate)
def get_corporate_by_id(corporate_id: str, db: Session = Depends(get_db)):
    corporate = crud.get_corporate(db, corporate_id=corporate_id)
    if corporate is None:
        raise HTTPException(status_code=404, detail="Corporate does not exist.")
    return corporate

### GET BENEFICIARY BASED ON BENEFICIARY ID ###
@app.get('/beneficiary/{beneficiary_id}', response_model=schemas.Beneficiary)
def get_beneficiary_by_id(beneficiary_id: str, db: Session = Depends(get_db)):
    beneficiary = crud.get_beneficiary(db, beneficiary_id=beneficiary_id)
    if beneficiary is None:
        raise HTTPException(status_code=404, detail="Beneficiary does not exist.")
    return beneficiary

### GET SUBSCRIPTIONS BASED ON CORPORATE ID ###
@app.get('/subscription/corporate/{corporate_id}', response_model=List[schemas.Subscription])
def get_subscriptions_by_corporate(corporate_id: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100,):
    subscriptions = crud.get_subscriptions_by_corporate(db, corporate_id=corporate_id, skip=skip,limit=limit)

    return subscriptions

### GET SUBSCRIPTIONS BASED ON BENEFICIARY ID ###
@app.get('/subscription/beneficiary/{beneficiary_id}', response_model=List[schemas.Subscription])
def get_subscriptions_by_beneficiary(beneficiary_id: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100,):
    subscriptions = crud.get_subscriptions_by_beneficiary(db, beneficiary_id=beneficiary_id, skip=skip,limit=limit)

    if subscriptions is None:
        raise HTTPException(status_code=404, detail="Beneficiary is not subscribed to anyone.")

    return subscriptions

### GET SUBSCRIBERS INFO BASED ON CORPORATE ID ###
@app.get('/subscriber/corporate/{corporate_id}', response_model=List[schemas.Beneficiary])
def get_subscribers_information_by_corporate(corporate_id: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100,):
    subscriptions = crud.get_subscriptions_by_corporate(db, corporate_id=corporate_id, skip=skip,limit=limit)
    
    if subscriptions is None:
        raise HTTPException(status_code=404, detail="Corporate has no subscribers.")
    
    subscribers = []
    for s in subscriptions:
        subscribers.append(crud.get_beneficiary(db, beneficiary_id=s.beneficiary_id))

    return subscribers

### GET FAVOURITE ###
@app.get('/favourite')
def get_favourite(beneficiary_id: str, listing_id:str, db: Session = Depends(get_db)):
    favourite = crud.get_favourite(db, beneficiary_id=beneficiary_id, listing_id=listing_id)
    if favourite is None:
        return False
    return True

### DELETE STUFF!!! ###
### DELETE SINGLE FAVOURITE###
@app.delete('/favourite')
def delete_favourite(favourite: schemas.Favourite, db: Session = Depends(get_db)):
    return crud.delete_favourite(db, favourite=favourite)

### DELETE SINGLE FAVOURITE###
@app.delete('/subscription')
def delete_subscription(subscription: schemas.Subscription, db: Session = Depends(get_db)):
    return crud.delete_subscription(db, subscription=subscription)

@app.get('/all_favourite/{beneficiary_id}')
def get_all_favourites(beneficiary_id: str, db: Session = Depends(get_db)):
    favourites = crud.get_all_favourites(db, beneficiary_id=beneficiary_id)
    if favourites is None:
        return None
    return favourites

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8421)