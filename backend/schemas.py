'''pydantic models for fastapi'''
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class ReceiptBase(BaseModel):
    datetime: datetime
    store_id: str
    paymentmethod_id: str
    total: float
    id: str
    reprint: str
    etag: str


class Receipt(ReceiptBase):

    class Config:
        orm_mode = True


class ReceiptCreate(ReceiptBase):
    pass


class ProductBase(BaseModel):
    id: str


class Product(ProductBase):
    name: str

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass


class ReceiptlineBase(BaseModel):
    linenumber: int
    product_id: str
    amount: float
    receipt_id: str


class Receiptline(ReceiptlineBase):

    class Config:
        orm_mode = True


class ReceiptlineCreate(ReceiptlineBase):
    pass


class Chain(BaseModel):
    '''Not implementing separate model for creation, as ID needs to always be provided,
        at least as long as the DB relies on system keys as PKs. If and when this changes
        to generating uniform keys, this model should change as well.
    '''
    id: str
    name: str


class StoreBase(BaseModel):
    id: str
    name: str
    chain_id: str


class Store(StoreBase):

    class Config:
        orm_mode = True


class StoreCreate(StoreBase):
    pass


class Paymentmethod(BaseModel):
    id: str
    payer: Optional[str]
