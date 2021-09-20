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