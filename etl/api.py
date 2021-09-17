from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .models import Receipt
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
    return db.query(Receipt).all()


@app.get('/')
def root():
    return 'Hello there!'
