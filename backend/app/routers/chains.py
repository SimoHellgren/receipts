from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
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
    return crud.chain.get_many(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_chain(chain: schemas.Chain, db: Session = Depends(get_db)):
    return crud.chain.create(db, obj_in=chain)


@router.put('/{chain_id}/')
def update_chain(chain: schemas.Chain, db: Session = Depends(get_db)):
    '''Idempotent PUT operation: if resource already exists, it is updated. If not, it gets created'''
    # Chain exists already -> update
    db_chain = crud.chain.get(db, chain.id)
    if db_chain:
        new_chain = crud.chain.update(db, db_obj=db_chain, obj_in=chain)
        response_code = status.HTTP_200_OK

    # Otherwise chain is created
    else:
        new_chain = crud.chain.create(db, obj_in=chain)
        response_code=status.HTTP_201_CREATED
    
    return JSONResponse(status_code=response_code, content=jsonable_encoder(new_chain))
