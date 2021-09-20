from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import schemas
from . import models
from .database import SessionLocal

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_methods=['*']
)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


@app.get('/receipts')
def get_receipts(db: Session = Depends(get_db)):
    return db.query(models.Receipt).all()

@app.post('/receipts', status_code=status.HTTP_201_CREATED)
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

@app.get('/products')
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@app.get('/')
def root():
    return 'Hello there!'
