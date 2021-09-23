from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import receipts, products, stores, chains

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_methods=['*']
)

app.include_router(receipts.router)
app.include_router(products.router)
app.include_router(stores.router)
app.include_router(chains.router)

@app.get('/')
def root():
    return 'Hello there!'
