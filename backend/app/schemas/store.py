from pydantic import BaseModel


class StoreBase(BaseModel):
    id: str
    name: str
    chain_id: str


class Store(StoreBase):

    class Config:
        orm_mode = True


class StoreCreate(StoreBase):
    pass
