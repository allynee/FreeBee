from sqlalchemy.orm import Session
import models
import schemas
from fastapi.encoders import jsonable_encoder
from typing import Dict, Union, Any
import datetime
from fastapi import HTTPException

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

def update_listing(db: Session, listing_id: int, data: schemas.ListingUpdate):
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

# def update_listing(db: Session, db_obj: models.Listing, obj_in: Union[schemas.ListingUpdate, Dict[str, Any]]) -> models.Listing:
#     obj_data = jsonable_encoder(db_obj)
#     if isinstance(obj_in, dict):
#         update_data = obj_in
#     else:
#         update_data = obj_in.dict(exclude_unset=True)
#     for field in obj_data:
#         if field in update_data:
#             setattr(db_obj, field, update_data[field])
#     db_obj.modified = datetime.now()
#     db.add(db_obj)
#     db.commit()
#     db.refresh(db_obj)
#     return db_obj

# def update_listing(db:Session, listing_id: int, new_qty: int, listing:schemas.Listing):
#     listing = get_listing(listing_id)
#     listing.quantity = new_qty
#     db.add(listing)
#     db.commit()
#     db.refresh(listing)
#     return listing

# def update_reservation(db: Session, db_obj: models.Reservation,
#     obj_in: Union[schemas.ReservationUpdate, Dict[str, Any]],
# ) -> models.Reservation:
#     obj_data = jsonable_encoder(db_obj)

#     if isinstance(obj_in, dict):
#         update_data = obj_in
#     else:
#         update_data = obj_in.dict(exclude_unset=True)
#     for field in obj_data:
#         if field in update_data:
#             setattr(db_obj, field, update_data[field])
#     db_obj.updated_at = datetime.now()
#     db.add(db_obj)
#     db.commit()
#     db.refresh(db_obj)
#     return db_obj