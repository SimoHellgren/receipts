from pydantic import BaseModel


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
