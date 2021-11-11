from pydantic import BaseModel

class Receiptline(BaseModel):
    linenumber: int
    product_id: str
    amount: float
    receipt_id: str
