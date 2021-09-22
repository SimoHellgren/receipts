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


class ReceiptlineBase(BaseModel):
    linenumber: int
    product_id: str
    amount: float


class Receiptline(ReceiptlineBase):
    receipt_id: str
    datetime: datetime
    store_id: str
    paymentmethod_id: str

    class Config:
        orm_mode = True

class ReceiptlineCreate(ReceiptlineBase):
    pass
