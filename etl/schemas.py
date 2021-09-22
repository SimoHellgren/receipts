'''pydantic models for fastapi'''
from datetime import datetime

from pydantic import BaseModel

class ReceiptBase(BaseModel):
    datetime: datetime
    store_id: str
    paymentmethod_id: str
    total: float


class Receipt(ReceiptBase):
    id: str
    reprint: str
    etag: str

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


class Receiptline(BaseModel):
    receipt_id: str
    linenumber: int
    datetime: datetime
    store_id: str
    product_id: str
    paymentmethod_id: str
    amount: float

    class Config:
        orm_mode = True
