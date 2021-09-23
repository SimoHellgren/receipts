from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import models

router = APIRouter(
    prefix='/stores',
    tags=['Stores']
)

@router.get('/')
def get_stores(db: Session = Depends(get_db)):
    return db.query(models.Store).all()
