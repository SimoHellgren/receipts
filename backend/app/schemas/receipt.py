from datetime import datetime

from pydantic import BaseModel, StrictInt

class ReceiptBase(BaseModel):
    datetime: datetime
    store_id: str
    paymentmethod_id: str
    total: StrictInt
    id: str
    reprint: str
    etag: str


class Receipt(ReceiptBase):

    class Config:
        orm_mode = True


class ReceiptCreate(ReceiptBase):
    pass
