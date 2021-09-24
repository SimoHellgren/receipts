from sqlalchemy.orm import Session

from . import models
from . import schemas

def get_chains(db: Session):
    return db.query(models.Chain).all()

def create_chain(db: Session, chain: schemas.Chain):
    db_chain = models.Chain(
        id=chain.id,
        name=chain.name
    )

    db.add(db_chain)
    db.commit()
    db.refresh(db_chain)

    return db_chain