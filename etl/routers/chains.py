from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import models
from .. import schemas

router = APIRouter(
    prefix='/chains',
    tags=['Chains']
)

@router.get('/')
def get_chains(db: Session = Depends(get_db)):
    return db.query(models.Chain).all()

@router.post('/')
def create_chain(chain: schemas.Chain, db: Session = Depends(get_db)):
    db_chain = models.Chain(
        id=chain.id,
        name=chain.name
    )

    db.add(db_chain)
    db.commit()
    db.refresh(db_chain)

    return db_chain
