import datetime
from typing import Union, Optional
from pydantic import BaseModel

class ListingBase(BaseModel):
    listing_id: str
    corporate_id: str
    corporate_name: str
    name: str
    description: Optional[str] = None
    collection_details: str
    address: str
    postal: Optional[int] = None
    district: Optional[int] = None
    area: Optional[str] = None
    category: str
    quantity: int
    status: str 
    img_ext: Optional[str] = None

class Listing(ListingBase):
    created: datetime.datetime
    modified: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True

class ListingCreate(ListingBase):
    pass

class ListingUpdate(ListingBase):
    __annotations__ = {k: Optional[v] for k, v in ListingCreate.__annotations__.items()}
