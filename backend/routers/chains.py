from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import crud
from .. import schemas


router = APIRouter(
    prefix='/chains',
    tags=['Chains']
)

@router.get('/')
def get_chains(db: Session = Depends(get_db)):
    return crud.get_chains(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_chain(chain: schemas.Chain, db: Session = Depends(get_db)):
    return crud.create_chain(db, chain)
