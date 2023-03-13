'''
Here core functions are defined for different operations.
'''

from typing import Dict
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal, engine
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
# @app.get('/listing', response_model=schemas.ListingBase)
# async def get_all_listings(db: Session = Depends(get_db)):
#     try:
#         listing = db.query(models.Listing).all()
#         if not listing:
#             raise HTTPException(status_code=404, detail="Listing not found")
#         return listing
#     except SQLAlchemyError as e:
#         raise HTTPException(status_code=500, detail=e)
    
@app.get('/listing', response_model=schemas.ListingBase)
def get_all_listings(db: Session = Depends(get_db)):
    listing = db.query(models.Listing).all()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing
    # except SQLAlchemyError as e:
    #     raise HTTPException(status_code=500, detail=e)

### GET SINGLE LISTING BASED ON LISTING ID ###
@app.get('/listing/{listing_id}', response_model=schemas.ListingBase)
async def get_listing_by_id(listing_id: int, db: Session = Depends(get_db)):
    try: 
        listing = db.query(models.Listing).filter(models.Listing.listing_id==listing_id).first()
        if not listing:
            raise HTTPException(status_code=404, detail="Listing not found")
        return listing 
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=e)
    
### CREATE SINGLE LISTING ###
@app.post('/listing')
async def create_listing(item: schemas.ListingCreate, db: Session = Depends(get_db)):
    db_item = models.Listing(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

# To run with debug: uvicorn main:app --reload --host 0.0.0.0 --port 8000
