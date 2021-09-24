from fastapi import APIRouter, Depends
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
    return crud.get_paymentmethods(db)


@router.post('/')
def create_paymentmethod(paymentmethod: schemas.Paymentmethod, db: Session = Depends(get_db)):
    return crud.create_paymentmethod(db, paymentmethod)
