from datetime import datetime

from pydantic import BaseModel, StrictInt


class ReceiptCreate(BaseModel):
    id: str
    datetime: datetime 
    store_id: str
    paymentmethod_id: str
    total: StrictInt
    reprint: str
    etag: str
