from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

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
