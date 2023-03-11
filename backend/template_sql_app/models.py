'''
Database tables Classes are defined here
'''

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Corporate(Base):
    __tablename__ = 'corporate'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(20), nullable=False, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(String(5000), nullable=False, index=True)

    def __init__(self, id, email, password, name, description):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.description = description 
    
    def json(self):
        return {
            "id": self.id,
            "email": self.title,
            "password": self.password,
            "name": self.name,
            "description": self.description
        }

class Listing(Base):
    __tablename__ = 'listing'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(100), nullable = False, index=True)
    corporate_id = Column(Integer, ForeignKey('corporate.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = Column(String(200), nullable=False, index=True)
    category = Column(String(200), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, index=True)
    collection_details = description = Column(String(10000), nullable=False, index=True)


'''
Below are some templates from online
'''

# database table
# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False, index=True)
#     email = Column(String(100), nullable=False, unique=True, index=True)
#     address = Column(String(100), nullable=False)
#     hashed_password = Column(String(100), nullable=False)
#     is_active = Column(Boolean, default=True)
#     items = relationship("Item", back_populates="owner")

# # database table
# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(100), nullable=False, index=True)
#     description = Column(String(100), nullable=False, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
#     owner = relationship("User", back_populates="items")