from sqlalchemy.orm import Session
import models
import schemas
from fastapi.encoders import jsonable_encoder
from typing import Dict, Union, Any
import datetime
from fastapi import HTTPException

### BENEFICIARY TABLE ###
def get_beneficiary(db: Session, beneficiary_id: int):
    return db.query(models.Beneficiary).filter(models.Beneficiary.beneficiary_id == beneficiary_id).first()

def get_all_beneficiaries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Beneficiary).offset(skip).limit(limit).all()

def create_beneficiary(db: Session, beneficiary: schemas.BeneficiaryCreate):
    beneficiary = models.Beneficiary(**beneficiary.dict())
    db.add(beneficiary)
    db.commit() 
    db.refresh(beneficiary)
    return beneficiary

def update_beneficiary(db: Session, beneficiary_id: int, data: schemas.BeneficiaryUpdate):
    beneficiary= db.query(models.Beneficiary).filter(models.Beneficiary.beneficiary_id == beneficiary_id).first()

    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiary not found")

    for field, value in vars(data).items():
        if value is not None:
            setattr(beneficiary, field, value)

    db.add(beneficiary)
    db.commit()
    db.refresh(beneficiary)

    return beneficiary

def delete_beneficiary(db: Session, beneficiary_id: int):
    beneficiary = db.query(models.Beneficiary).filter(models.Beneficiary.beneficiary_id == beneficiary_id).first()

    if not beneficiary:
        # return{
        #     "code": 404,
        #     "message": "Listing not found"
        # }
        raise HTTPException(status_code=404, detail="Listing not found")

    db.delete(beneficiary)
    db.commit()

    return {
        "code": 200,
        "message": "Listing deleted successfully"
    }

### PREFERENCE TABLE ###
def get_all_preferences(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Preference).offset(skip).limit(limit).all()

def create_preference(db: Session, preference: schemas.PreferenceCreate):
    preference = models.Preference(**preference.dict())
    db.add(preference)
    db.commit() 
    db.refresh(preference)
    return preference

def delete_preference(db: Session, beneficiary_id: int, category: str):
    preference = db.query(models.Beneficiary).filter(models.Beneficiary.beneficiary_id == beneficiary_id,
                                                      models.Beneficiary.category == category).first()

    if not preference:
        # return{
        #     "code": 404,
        #     "message": "Listing not found"
        # }
        raise HTTPException(status_code=404, detail="Preference not found")

    db.delete(preference)
    db.commit()

    return {
        "code": 200,
        "message": "Preference deleted successfully"
    }

### SUBSCRIPTION TABLE ###
def get_all_subscriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subscription).offset(skip).limit(limit).all()

def create_subscription(db: Session, subscription: schemas.SubscriptionCreate):
    subscription = models.Subscription(**subscription.dict())
    db.add(subscription)
    db.commit() 
    db.refresh(subscription)
    return subscription

def delete_subscription(db: Session, beneficiary_id: int, corporate_id: int):
    subscription = db.query(models.Subscription).filter(models.Subscription.beneficiary_id == beneficiary_id,
                                                       models.Subscription.corporate_id == corporate_id).first()
    if not subscription:
        # return{
        #     "code": 404,
        #     "message": "Listing not found"
        # }
        raise HTTPException(status_code=404, detail="Subscription not found")

    db.delete(subscription)
    db.commit()

    return {
        "code": 200,
        "message": "Subscription deleted successfully"
    }

### FAVOURITE TABLE ###
def get_all_favourites(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Favourite).offset(skip).limit(limit).all()

def create_favourite(db: Session, favourite: schemas.FavouriteCreate):
    favourite = models.Favourite(**favourite.dict())
    db.add(favourite)
    db.commit() 
    db.refresh(favourite)
    return favourite

def delete_favourite(db: Session, beneficiary_id: int, listing_id: int):
    favourite = db.query(models.Favourite).filter(models.Favourite.beneficiary_id == beneficiary_id,
                                                  models.Favourite.listing_id == listing_id).first()

    if not favourite:
        # return{
        #     "code": 404,
        #     "message": "Listing not found"
        # }
        raise HTTPException(status_code=404, detail="Favourite not found")

    db.delete(favourite)
    db.commit()

    return {
        "code": 200,
        "message": "Favourite deleted successfully"
    }