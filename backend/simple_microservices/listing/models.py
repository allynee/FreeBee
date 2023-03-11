'''
Database tables Classes are defined here
'''
import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base

class Listing(Base):
    __tablename__ = 'listing'
    listing_id = Column(Integer, primary_key=True, index=True)
    corporate_id = Column(Integer, ForeignKey('corporate.corporate_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False, index=True)
    description = Column(String(5000), nullable=False, index=True)
    collection_details = Column(String(5000), nullable=False, index=True)
    address = Column(String(100), nullable = False, index=True)
    postal= Column(Integer, nullable = False, index=True)
    district = Column(Integer, nullable = False, index=True)
    category = Column(String(50), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, index=True)
    nlp_1 = Column(String(50), nullable=False, index=True)
    nlp_2 = Column(String(50), nullable=False, index=True)
    nlp_3 = Column(String(50), nullable=False, index=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    modified = Column(DateTime(timezone=True), onupdate=func.now())