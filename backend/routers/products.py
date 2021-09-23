from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import models
from .. import schemas


router = APIRouter(
    prefix='/products',
    tags=['Products']
)

@router.get('/')
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product=models.Product(
        id=product.id,
        name=None
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product
