from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import crud
from .. import schemas


router = APIRouter(
    prefix='/stores',
    tags=['Stores']
)

@router.get('/')
def get_stores(db: Session = Depends(get_db)):
    return crud.get_stores(db)


@router.get('/{store_id}')
def get_store(store_id: str, db = Depends(get_db)):
    return crud.get_store(db, store_id)


@router.post('/')
def create_store(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    return crud.create_store(db, store)
