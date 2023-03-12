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

### FIND SINGLE LISTING BASED ON LISTING ID ###
# @app.get('/listing/{listing_id}', response_model=None)
# async def get_listing_by_id(listing_id: int, db: Session = Depends(get_db)):
#     try:
#         return db.query(models.Listing).all()
#         print(listing)
#         if not listing:
#             raise HTTPException(status_code=404, detail="Listing not found")
#         return listing 
#     except SQLAlchemyError:
#         raise HTTPException(status_code=500, detail="Database error")
    
@app.get('/listing/{listing_id}', response_model=None)
async def get_listing_by_id(listing_id: int, db: Session = Depends(get_db)):
    try: 
        # db = SessionLocal()
        listing = db.query(models.Listing).all()
            # listing = db.query(models.Listing).filter(models.Listing.listing_id==listing_id).first()
            # listing = models.Listing.query.filter_by(models.Listing.listing_id==listing_id).first()
        if not listing:
            raise HTTPException(status_code=404, detail="Listing not found")
        # db.close()
        return listing 
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=e)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)