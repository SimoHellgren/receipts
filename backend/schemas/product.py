from pydantic import BaseModel


class ProductBase(BaseModel):
    id: str


class Product(ProductBase):
    name: str

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass
