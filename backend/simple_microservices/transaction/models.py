'''
Database tables Classes are defined here
'''

import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base

class Transaction(Base):
    __tablename__ = 'transaction'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    listing_id = Column(Integer, nullable=False, index=True)
    corporate_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    status = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False, index=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    modified = Column(DateTime(timezone=True), onupdate=func.now())