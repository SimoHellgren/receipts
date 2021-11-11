from pydantic import BaseModel, StrictInt


class ReceiptlineBase(BaseModel):
    linenumber: int
    product_id: str
    amount: StrictInt
    receipt_id: str


class Receiptline(ReceiptlineBase):

    class Config:
        orm_mode = True


class ReceiptlineCreate(ReceiptlineBase):
    pass
