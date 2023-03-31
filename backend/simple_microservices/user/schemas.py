import datetime
from typing import Union, Optional
from pydantic import BaseModel

### BENEFICIARY ###

class BeneficiaryBase(BaseModel):
    beneficiary_id: int
    email: str
    username: str
    phone: Optional[int] = None
    address: Optional[str] = None
    postal: Optional[int] = None
    district: Optional[int] = None 
    area: Optional[str] = None

class Beneficiary(BeneficiaryBase):

    class Config:
        orm_mode = True

class BeneficiaryCreate(BeneficiaryBase):
    pass

class BeneficiaryUpdate(BeneficiaryBase):
    __annotations__ = {k: Optional[v] for k, v in BeneficiaryCreate.__annotations__.items()}

### CORPORATE ###

class CorporateBase(BaseModel):
    corporate_id: int
    email: str
    name: str
    description: Optional[str] = None

class Corporate(CorporateBase):

    class Config:
        orm_mode = True

class CorporateCreate(CorporateBase):
    pass

class CorporateUpdate(CorporateBase):
    __annotations__ = {k: Optional[v] for k, v in CorporateCreate.__annotations__.items()}

### PREFERENCE ###

class PreferenceBase(BaseModel):
    beneficiary_id: int
    category: str 

class Preference(PreferenceBase):
    
    class Config:
        orm_mode = True

class PreferenceCreate(PreferenceBase):
    pass

class PreferenceUpdate(PreferenceBase):
    __annotations__ = {k: Optional[v] for k, v in PreferenceCreate.__annotations__.items()}


### SUBSCRIPTION ###

class SubscriptionBase(BaseModel):
    beneficiary_id: int
    corporate_id: int

class Subscription(SubscriptionBase):
    class Config:
        orm_mode = True

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    __annotations__ = {k: Optional[v] for k, v in SubscriptionCreate.__annotations__.items()}


### FAVOURITE ###

class FavouriteBase(BaseModel):
    beneficiary_id: int
    listing_id: int

class Favourite(FavouriteBase):
    class Config:
        orm_mode = True

class FavouriteCreate(FavouriteBase):
    pass

class FavouriteUpdate(FavouriteBase):
    __annotations__ = {k: Optional[v] for k, v in FavouriteCreate.__annotations__.items()}

