'''
Database connection is defined here
'''

import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://admin1:12345678@esdeeznutspublic.cwjfrbjqz4fp.ap-southeast-1.rds.amazonaws.com:3306/beneficiary'   

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
