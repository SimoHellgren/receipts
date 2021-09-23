from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import models
from .. import schemas

router = APIRouter(
    prefix='/stores',
    tags=['Stores']
)

@router.get('/')
def get_stores(db: Session = Depends(get_db)):
    return db.query(models.Store).all()

@router.post('/')
def create_store(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    # generate a store id from chain id and store name. Use also as store_name,
    # for the sake of consistency, at least for now
    store_id = store_name = f'{store.chain_id} {store.name}'

    db_store = models.Store(
        id=store_id,
        name=store_name,
        chain_id=store.chain_id
    )

    db.add(db_store)
    db.commit()
    db.refresh(db_store)

    return db_store
