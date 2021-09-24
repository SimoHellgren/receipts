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


def get_stores(db: Session):
    return db.query(models.Store).all()


def create_store(db: Session, store: schemas.StoreCreate):
    db_store = models.Store(
        id=store.id,
        name=store.name,
        chain_id=store.chain_id
    )

    db.add(db_store)
    db.commit()
    db.refresh(db_store)

    return db_store
