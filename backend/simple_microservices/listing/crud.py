from sqlalchemy.orm import Session
import models
import schemas
from fastapi.encoders import jsonable_encoder
from typing import Dict, Union, Any
import datetime
from fastapi import HTTPException

def get_listing(db: Session, listing_id: str):
    return db.query(models.Listing).filter(models.Listing.listing_id == listing_id).first()

def get_listings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Listing).offset(skip).limit(limit).all()

def create_listing(db: Session, listing: schemas.ListingCreate):
    listing = models.Listing(**listing.dict())
    db.add(listing)
    db.commit() 
    db.refresh(listing)
    return listing

def update_listing(db: Session, listing_id: str, data: schemas.ListingUpdate):
    listing = db.query(models.Listing).filter(models.Listing.listing_id == listing_id).first()

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    for field, value in vars(data).items():
        if value is not None:
            setattr(listing, field, value)

    db.add(listing)
    db.commit()
    db.refresh(listing)

    return listing

def delete_listing(db: Session, listing_id: str):
    listing= db.query(models.Listing).filter(models.Listing.listing_id == listing_id).first()

    if not listing:
        return{
            "code": 404,
            "message": "Listing not found"
        }
        # raise HTTPException(status_code=404, detail="Listing not found")

    db.delete(listing)
    db.commit()

    return {
        "code": 200,
        "message": "Listing deleted successfully"
    }

def get_corporate_listings(db: Session,corporate_id: str ,skip: int = 0, limit: int = 100):
    return db.query(models.Listing).filter(models.Listing.corporate_id == corporate_id).offset(skip).limit(limit).all()