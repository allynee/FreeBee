from sqlalchemy.orm import Session
import models
import schemas

def get_listing(db: Session, listing_id: int):
    return db.query(models.Listing).filter(models.Listing.listing_id == listing_id).first()

def get_listings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Listing).offset(skip).limit(limit).all()

def create_listing(db: Session, listing: schemas.ListingCreate):
    listing = models.Listing(**listing.dict())
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing