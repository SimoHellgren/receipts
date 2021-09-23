from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import models

router = APIRouter(
    prefix='/chains',
    tags=['Chains']
)

@router.get('/')
def get_chains(db: Session = Depends(get_db)):
    return db.query(models.Chain).all()
