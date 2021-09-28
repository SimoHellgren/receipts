from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import crud
from .. import schemas


router = APIRouter(
    prefix='/receipts',
    tags=['Receipts']
)

@router.get('/')
def get_receipts(db: Session = Depends(get_db)):
    return crud.receipt.get_many(db)


@router.get('/{receipt_id}')
def get_receipt(receipt_id: str, db: Session = Depends(get_db)):
    db_receipt = crud.receipt.get(db, receipt_id)
    
    if not db_receipt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Receipt not found')

    return db_receipt


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_receipt(receipt: schemas.ReceiptCreate, db: Session = Depends(get_db)):
    return crud.receipt.create(db, obj_in=receipt)


@router.put('/{receipt_id}')
def update_receipt(receipt_id: str, receipt: schemas.Receipt, db: Session = Depends(get_db)):
    db_obj = crud.receipt.get(db, receipt_id)

    if db_obj:
        response_code = status.HTTP_200_OK
        new_obj = crud.receipt.update(db, db_obj=db_obj, obj_in=receipt)
    
    else:
        response_code = status.HTTP_201_CREATED
        new_obj = crud.receipt.create(db, obj_in=receipt) # techincally receipt isn't the type obj_in expects
    
    return JSONResponse(status_code=response_code, content=jsonable_encoder(new_obj))


@router.get('/{receipt_id}/lines', response_model=List[schemas.Receiptline])
def get_receipt_lines(receipt_id: str, db: Session = Depends(get_db)):
    db_receiptlines = crud.receiptline.get_by_receipt(db, receipt_id)

    if not db_receiptlines:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Receipt lines not found')

    return db_receiptlines


@router.post('/{receipt_id}/lines', status_code=status.HTTP_201_CREATED)
def create_receipt_line(receipt_id: str, line: schemas.ReceiptlineCreate, db: Session = Depends(get_db)):
    return crud.receiptline.create(db, obj_in=line)
