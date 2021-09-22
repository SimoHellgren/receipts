from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import models
from .. import schemas

router = APIRouter(
    prefix='/receipts',
    tags=['Receipts']
)

@router.get('/')
def get_receipts(db: Session = Depends(get_db)):
    return db.query(models.Receipt).all()


@router.get('/{receipt_id}')
def get_receipt(receipt_id: str, db: Session = Depends(get_db)):
    db_receipt = db.query(models.Receipt).get(receipt_id)
    
    if not db_receipt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Receipt not found')

    return db_receipt


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_receipt(receipt: schemas.ReceiptCreate, db: Session = Depends(get_db)):
    id = 'testreceipt'
    reprintlines = [
        'This is a custom made receipt',
        "It doesn't really have a reprint,",
        "but here we are anyways.",
        "",
        "Bye!"
    ]
    db_receipt = models.Receipt(
        id=id,
        reprint='\n'.join(l.center(42) for l in reprintlines),
        total=receipt.total,
        etag=None,
        datetime=receipt.datetime,
        store_id=receipt.store_id,
        paymentmethod_id=receipt.paymentmethod_id
    )

    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    return db_receipt


@router.get('/{receipt_id}/lines', response_model=List[schemas.Receiptline])
def get_receipt_lines(receipt_id: str, db: Session = Depends(get_db)):
    db_receiptlines = db.query(models.Receiptline).filter(
        models.Receiptline.receipt_id == receipt_id
    ).order_by(models.Receiptline.linenumber).all()

    if not db_receiptlines:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Receipt lines not found')

    return db_receiptlines
