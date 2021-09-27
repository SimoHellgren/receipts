from typing import List

from sqlalchemy.orm import Session

from .. import models
from .. import schemas


def get_products(db: Session):
    return db.query(models.Product).all()

def get_product(db: Session, product_id: str):
    return db.query(models.Product).get(product_id)



def create_product(db: Session, product: schemas.ProductCreate):
    db_product=models.Product(
        id=product.id,
        name=None
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_receipts(db: Session):
    return db.query(models.Receipt).all()


def get_receipt(db: Session, receipt_id: str):
    return db.query(models.Receipt).get(receipt_id)


def create_receipt(db: Session, receipt: schemas.ReceiptCreate):
    db_receipt = models.Receipt(
        id=receipt.id,
        total=receipt.total,
        etag=receipt.etag,
        datetime=receipt.datetime,
        store_id=receipt.store_id,
        paymentmethod_id=receipt.paymentmethod_id,
        reprint=receipt.reprint
    )

    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)

    return db_receipt

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
