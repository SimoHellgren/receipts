from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ..dependencies import get_db
from .. import crud
from .. import schemas


router = APIRouter(
    prefix='/paymentmethods',
    tags=['Paymentmethods']
)

@router.get('/')
def get_paymentmethods(db: Session = Depends(get_db)):
    return crud.paymentmethod.get_many(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_paymentmethod(paymentmethod: schemas.Paymentmethod, db: Session = Depends(get_db)):
    return crud.paymentmethod.create(db, obj_in=paymentmethod)


@router.put('/{paymentmethod_id}')
def update_paymentmethod(paymentmethod_id: str, paymentmethod: schemas.Paymentmethod, db: Session = Depends(get_db)):
    db_obj = crud.paymentmethod.get(db, paymentmethod_id)

    if db_obj:
        response_code = status.HTTP_200_OK
        new_obj = crud.paymentmethod.update(db, db_obj=db_obj, obj_in=paymentmethod)

    else:
        response_code = status.HTTP_201_CREATED
        new_obj = crud.paymentmethod.create(db, obj_in=paymentmethod)

    return JSONResponse(status_code=response_code, content=jsonable_encoder(new_obj))
