from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    id: str


class Product(ProductBase):
    name: Optional[str]

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass
