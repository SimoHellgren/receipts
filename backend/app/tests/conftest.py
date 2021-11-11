import os
from datetime import datetime

from dotenv import load_dotenv
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from fastapi.testclient import TestClient

from backend.app.api import app
from backend.app.db.base_class import Base
from backend.app.dependencies import get_db
from backend.app import models


load_dotenv()

engine = create_engine(os.environ['TEST_DB_URI'])

def make_test_data():
     return {
        'chain': models.Chain(id='CHAIN_1', name='Chain 1'),
        'store': models.Store(id='STORE_1', name='Store 1', chain_id='CHAIN_1'),
        'paymentmethod': models.Paymentmethod(id='CASH', payer=None),
        'receipt': models.Receipt(
            datetime=datetime(2021, 1, 1, 0, 0, 0, 0),
            store_id='STORE_1',
            paymentmethod_id='CASH',
            total=1111,
            id='RECEIPT_1',
            reprint='Test reprint',
            etag='iuyweriuyweriuyhsdkjhskjfh'
        ),
        'product': models.Product(id='PRODUCT_1', name='Product 1'),
        'line1': models.Receiptline(receipt_id='RECEIPT_1', linenumber=1, product_id='PRODUCT_1', amount=1.15),
        'line2': models.Receiptline(receipt_id='RECEIPT_1', linenumber=2, product_id='PRODUCT_1', amount=1.15)
    }

@pytest.fixture
def test_data():
    return make_test_data()


def get_test_db():
    SessionLocal = sessionmaker(bind=engine)
    test_db = SessionLocal()

    for v in make_test_data().values():
        test_db.add(v)
        test_db.flush()

    try:
        yield test_db

    finally:
        # drop all data after each test
        for tbl in reversed(Base.metadata.sorted_tables):
            engine.execute(tbl.delete())
        test_db.close()


@pytest.fixture
def test_db_session():
    yield from get_test_db()


@pytest.fixture(scope='session', autouse=True)
def create_test_db():
    '''Whips up a fresh DB for testing, controlled by TEST_DB_URI.
        Note, if a DB exists with the same name, it is dropped, so
        take care when naming it.
    '''

    if database_exists(engine.url):
        drop_database(engine.url)

    create_database(engine.url)

    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = get_test_db

    yield # tests run at this point

    drop_database(engine.url)


@pytest.fixture(autouse=True)
def client():
    with TestClient(app) as c:
        yield c
