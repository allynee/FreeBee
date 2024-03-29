'''
Database tables Classes are defined here
'''

import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base

class Listing(Base):
    __tablename__ = 'listing'
    listing_id = Column(String(200), primary_key=True, index=True)
    corporate_id = Column(String(200), nullable=False, index=True)
    corporate_name = Column(String(50), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(1000), nullable=False)
    collection_details = Column(String(5000), nullable=False, index=True)
    address = Column(String(200), nullable = False)
    postal= Column(Integer, nullable = False)
    district = Column(Integer, nullable = False, index=True)
    area = Column(String(50), nullable = False)
    category = Column(String(50), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, index=True)
    status = Column(String(50), nullable=False)
    img_ext = Column(String(50))

    created = Column(DateTime(timezone=True), server_default=func.now())
    modified = Column(DateTime(timezone=True),  onupdate=func.now())