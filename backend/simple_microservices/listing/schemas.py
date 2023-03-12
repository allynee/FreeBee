import datetime
from typing import Optional
from pydantic import BaseModel

# Optional[str] = None

class ListingBase(BaseModel):
    listing_id: int
    corporate_id: int
    name: str
    description: str
    collection_details: str
    address: str
    postal: int
    district: int
    category: int
    quantity: int
    nlp_1: str
    nlp_2: str
    nlp_3: str
    created: datetime.datetime
    modified: datetime.datetime

class ListingCreate(ListingBase):
    pass

class ListingUpdate(ListingBase):
    pass