from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import models

router = APIRouter(
    prefix='/paymentmethods',
    tags=['Paymentmethods']
)

@router.get('/')
def get_paymentmethods(db: Session = Depends(get_db)):
    return db.query(models.Paymentmethod).all()
