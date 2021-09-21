from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .routers import receipts
from . import models
from .dependencies import get_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_methods=['*']
)

app.include_router(receipts.router)

@app.get('/products')
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@app.get('/')
def root():
    return 'Hello there!'
