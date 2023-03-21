# To run with debug: uvicorn main: app --reload --host 0.0.0.0 --port 8421

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

### CREATE SINGLE BENEFICIARY ###
@app.post('/beneficiary', response_model=schemas.Beneficiary)
def create_beneficiary(beneficiary: schemas.BeneficiaryCreate, db: Session = Depends(get_db)):
    return crud.create_beneficiary(db, beneficiary=beneficiary)



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8421)