'''pydantic models for fastapi'''
from datetime import datetime


from pydantic import BaseModel


class Receipt(BaseModel):
    id: str
    reprint: str
    total: float
    etag: str
    datetime: datetime
    store_id: str
    paymentmethod_id: str