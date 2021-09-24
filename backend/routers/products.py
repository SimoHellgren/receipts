from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import crud
from .. import schemas


router = APIRouter(
    prefix='/products',
    tags=['Products']
)

@router.get('/')
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)
