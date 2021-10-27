from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import crud
from .. import schemas


router = APIRouter(
    prefix='/products',
    tags=['Products']
)

@router.get('/', response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    return crud.product.get_many(db)


@router.post('/', response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.product.create(db, obj_in=product)


@router.put('/{product_id}', response_model=schemas.Product)
def update_product(product_id: str, product: schemas.Product, db: Session = Depends(get_db)):
    db_obj = crud.product.get(db, product_id)

    if db_obj:
        response_code = status.HTTP_200_OK
        new_obj = crud.product.update(db, db_obj=db_obj, obj_in=product)

    else:
        response_code = status.HTTP_201_CREATED
        new_obj = crud.product.create(db, obj_in=product)

    return JSONResponse(status_code=response_code, content=jsonable_encoder(new_obj))
