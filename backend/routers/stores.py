from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ..dependencies import get_db
from .. import crud
from .. import schemas


router = APIRouter(
    prefix='/stores',
    tags=['Stores']
)

@router.get('/')
def get_stores(db: Session = Depends(get_db)):
    return crud.store.get_many(db)


@router.get('/{store_id}')
def get_store(store_id: str, db = Depends(get_db)):
    return crud.store.get(db, store_id)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_store(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    return crud.store.create(db, obj_in=store)


@router.put('/{store_id}')
def update_store(store_id: str, store: schemas.Store, db: Session = Depends(get_db)):
    db_store = crud.store.get(db, store_id)

    if db_store:
        response_code = status.HTTP_200_OK
        new_store = crud.store.update(db, db_obj=db_store, obj_in=store)

    else:
        response_code = status.HTTP_201_CREATED
        new_store = crud.store.create(db, obj_in=store)

    return JSONResponse(
        status_code=response_code,
        content=jsonable_encoder(new_store)
    )
