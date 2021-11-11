from pydantic import BaseModel

class Receiptline(BaseModel):
    linenumber: int
    product_id: str
    amount: int
    receipt_id: str
