from pydantic import BaseModel, StrictInt

class Receiptline(BaseModel):
    linenumber: int
    product_id: str
    amount: StrictInt
    receipt_id: str
