import datetime
from typing import Union, Optional
from pydantic import BaseModel

class TransactionBase(BaseModel):
    listing_id: int
    corporate_id: int
    beneficiary_id: int
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
    __annotations__ = {k: Optional[v] for k, v in TransactionBase.__annotations__.items()}