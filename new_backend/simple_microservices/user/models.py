'''
Database tables Classes are defined here
'''

import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base

class Beneficiary(Base):
    __tablename__ = 'beneficiary'
    beneficiary_id = Column(String(200), primary_key=True, index=True)
    email = Column(String(50), nullable=False, index=True)
    username = Column(String(50), nullable=False, index=True)
    phone= Column(Integer, index=True)
    address = Column(String(200), index=True)
    postal= Column(Integer)
    district = Column(Integer, index=True)
    area = Column(String(50), index=True)

    preferences = relationship('Preference', back_populates='beneficiary')
    subscriptions = relationship('Subscription', back_populates='beneficiary')
    favourites = relationship('Favourite', back_populates='beneficiary')

class Preference(Base):
    __tablename__ = 'preference'
    beneficiary_id = Column(String(200), ForeignKey('beneficiary.beneficiary_id'), primary_key=True)
    category = Column(String(50), primary_key=True, nullable=False, index=True)

    beneficiary = relationship('Beneficiary', back_populates='preferences')

class Subscription(Base):
    __tablename__ = 'subscription'
    beneficiary_id = Column(String(200), ForeignKey('beneficiary.beneficiary_id'), primary_key=True)
    corporate_id = Column(String(200), primary_key=True, nullable=False, index=True)

    beneficiary = relationship('Beneficiary', back_populates='subscriptions')

class Favourite(Base):
    __tablename__ = 'favourite'
    beneficiary_id = Column(String(200), ForeignKey('beneficiary.beneficiary_id'), primary_key=True)
    listing_id = Column(String(200), primary_key=True, index=True)

    beneficiary = relationship('Beneficiary', back_populates='favourites')

class Corporate(Base):
    __tablename__ = 'corporate'
    corporate_id = Column(String(200), primary_key=True, index=True)
    email = Column(String(50), nullable=False, index=True)
    name = Column(String(50), nullable=False, index=True)
    description = Column(String(1000), index=True)
