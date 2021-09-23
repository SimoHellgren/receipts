from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import models
from .. import schemas

router = APIRouter(
    prefix='/paymentmethods',
    tags=['Paymentmethods']
)

@router.get('/')
def get_paymentmethods(db: Session = Depends(get_db)):
    return db.query(models.Paymentmethod).all()

@router.post('/')
def create_paymentmethod(paymentmethod: schemas.Paymentmethod, db: Session = Depends(get_db)):
    db_paymentmethod = models.Paymentmethod(
        id=paymentmethod.id,
        payer=paymentmethod.payer
    )

    db.add(db_paymentmethod)
    db.commit()
    db.refresh(db_paymentmethod)

    return db_paymentmethod
