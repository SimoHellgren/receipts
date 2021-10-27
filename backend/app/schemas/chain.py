from pydantic import BaseModel


class Chain(BaseModel):
    '''Not implementing separate model for creation, as ID needs to always be provided,
        at least as long as the DB relies on system keys as PKs. If and when this changes
        to generating uniform keys, this model should change as well.
    '''
    id: str
    name: str

    class Config:
        orm_mode = True
