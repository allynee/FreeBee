import datetime
from typing import Union, Optional
from pydantic import BaseModel

class TransactionBase(BaseModel):
    listing_id: str
    corporate_id: str
    beneficiary_id: str
    status: str
    quantity: int

class Transaction(TransactionBase):
    transaction_id: int
    created: datetime.datetime
    modified: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    __annotations__ = {k: Optional[v] for k, v in TransactionCreate.__annotations__.items()}