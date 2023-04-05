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
@app.get('/listing', response_model=List[schemas.Listing])
def get_all_available_listings(skip: str = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_listings(db,skip=skip,limit=limit)
    if items is None:
        raise HTTPException(status_code=404, detail="No listings available")
    return items

### GET SINGLE LISTING BASED ON LISTING ID ###
@app.get('/listing/{listing_id}', response_model=schemas.Listing)
def get_listing_by_id(listing_id: str, db: Session = Depends(get_db)):
    listing = crud.get_listing(db, listing_id=listing_id)
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing
    
### CREATE SINGLE LISTING ###
@app.post('/listing', response_model=schemas.Listing)
def create_listing(listing: schemas.ListingCreate, db: Session = Depends(get_db)):
    return crud.create_listing(db, listing=listing)

### UPDATE ANY FIELD IN LISTING ###
@app.put('/listing/{listing_id}', response_model=schemas.Listing)
def update_listing(listing_id: str, listing: schemas.ListingUpdate, db: Session = Depends(get_db)):
    return crud.update_listing(db, listing_id=listing_id, data=listing)

### DELETE SINGLE LISTING ###
@app.delete('/listing/{listing_id}')
def delete_listing(listing_id: str, db: Session = Depends(get_db)):
    return crud.delete_listing(db, listing_id=listing_id)

@app.get('/listings/{corporate_id}', response_model=List[schemas.Listing])
def get_corporate_listings(corporate_id: str, db: Session = Depends(get_db)):
    listing = crud.get_corporate_listings(db, corporate_id=corporate_id)
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

### ASYNC DUMP?? dk if it's even correct ###
# async def get_listing_by_id(listing_id: int, db: Session = Depends(get_db)):
#     try: 
#         listing = db.query(models.Listing).filter(models.Listing.listing_id==listing_id).first()
#         if not listing:
#             raise HTTPException(status_code=404, detail="Listing not found")
#         return vars(listing)
#     except SQLAlchemyError as e:
#         raise HTTPException(status_code=500, detail=e)