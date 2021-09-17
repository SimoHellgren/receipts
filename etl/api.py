from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .models import Receipt
from .database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


@app.get('/receipts')
def get_receipts(db: Session = Depends(get_db)):
    return db.query(Receipt).all()


@app.get('/')
def root():
    return 'Hello there!'
