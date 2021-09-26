from typing import List

from sqlalchemy.orm import Session

from . import models
from . import schemas

def get_chains(db: Session):
    return db.query(models.Chain).all()

def create_chain(db: Session, chain: schemas.Chain):
    db_chain = models.Chain(
        id=chain.id,
        name=chain.name
    )

    db.add(db_chain)
    db.commit()
    db.refresh(db_chain)

    return db_chain


def get_stores(db: Session):
    return db.query(models.Store).all()


def create_store(db: Session, store: schemas.StoreCreate):
    db_store = models.Store(
        id=store.id,
        name=store.name,
        chain_id=store.chain_id
    )

    db.add(db_store)
    db.commit()
    db.refresh(db_store)

    return db_store


def get_paymentmethods(db: Session):
    return db.query(models.Paymentmethod).all()


def create_paymentmethod(db: Session, paymentmethod: schemas.Paymentmethod):
    db_paymentmethod = models.Paymentmethod(
        id=paymentmethod.id,
        payer=paymentmethod.payer
    )

    db.add(db_paymentmethod)
    db.commit()
    db.refresh(db_paymentmethod)

    return db_paymentmethod

def get_products(db: Session):
    return db.query(models.Product).all()


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