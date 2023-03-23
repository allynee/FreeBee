import datetime
from typing import Union, Optional
from pydantic import BaseModel

class TransactionBase(BaseModel):
    listing_id: int
    corporate_id: int
    user_id: int
    status: str

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class Transaction(TransactionBase):
    transaction_id: int
    created: datetime.datetime
    modified: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True