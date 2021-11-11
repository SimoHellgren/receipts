from typing import Optional

from pydantic import BaseModel


class Paymentmethod(BaseModel):
    id: str
    payer: Optional[str]

    class Config:
        orm_mode = True
