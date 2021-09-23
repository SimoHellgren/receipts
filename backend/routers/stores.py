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
    db_store = models.Store(
        id=store.id,
        name=store.name,
        chain_id=store.chain_id
    )

    db.add(db_store)
    db.commit()
    db.refresh(db_store)

    return db_store
