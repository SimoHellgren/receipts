from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import models

router = APIRouter(
    prefix='/products',
    tags=['Products']
)

@router.get('/')
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()
