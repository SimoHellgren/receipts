from typing import List

from sqlalchemy.orm import Session

from .. import models
from .. import schemas


def get_receiptlines(db: Session, receipt_id: str):
    '''This could use some linting'''
    return db.query(models.Receiptline).filter(
        models.Receiptline.receipt_id == receipt_id
    ).order_by(models.Receiptline.linenumber).all()


def create_receiptlines(db: Session, receipt_id: str, lines: List[schemas.ReceiptlineCreate]):
    db_receiptlines = [
        models.Receiptline(
            receipt_id=receipt_id,
            linenumber=line.linenumber,
            product_id=line.product_id,
            amount=line.amount
        )
        for line in lines
    ]

    db.add_all(db_receiptlines)
    db.commit()
    
    for line in db_receiptlines:
        db.refresh(line)

    return db_receiptlines
