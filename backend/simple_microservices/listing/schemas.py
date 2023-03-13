import datetime
from typing import Union, Optional
from pydantic import BaseModel

# Optional[str] = None

class ListingBase(BaseModel):
    corporate_id: int
    name: str
    description: str
    collection_details: str
    address: str
    postal: int
    district: int
    category: int
    quantity: int
    nlp_cat1: Optional[Union[str, None]] = None
    nlp_cat2: Optional[Union[str, None]] = None
    nlp_cat3: Optional[Union[str, None]] = None
    created: Optional[datetime.datetime] = None
    modified: Optional[datetime.datetime] = None

class ListingCreate(ListingBase):
    pass

class ListingUpdate(ListingBase):
    pass
