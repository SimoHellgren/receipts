import os
from datetime import datetime

from dotenv import load_dotenv
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from fastapi.testclient import TestClient

from backend.api import app
from backend.models import Base
from backend.dependencies import get_db
from backend import models

load_dotenv()

engine = create_engine(os.environ['TEST_DB_URI'])


def get_test_db():
    SessionLocal = sessionmaker(bind=engine)
    test_db = SessionLocal()

    try:
        yield test_db

    finally:
        test_db.close()


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


@pytest.fixture
def test_chain():
    return models.Chain(id='CHAIN_1', name='Chain 1')


@pytest.fixture
def test_store():
    return models.Store(id='STORE_1', name='Store 1', chain_id='CHAIN_1')


@pytest.fixture
def test_paymentmethod():
    return models.Paymentmethod(id='CASH', payer=None)


@pytest.fixture
def test_receipt():
    return models.Receipt(
        datetime=datetime(2021, 1, 1, 0, 0, 0, 0),
        store_id='STORE_1',
        paymentmethod_id='CASH',
        total=11.11,
        id='RECEIPT_1',
        reprint='Test reprint',
        etag='iuyweriuyweriuyhsdkjhskjfh'
    )


@pytest.fixture
def test_product():
    return models.Product(
        id='PRODUCT_1',
        name='Product 1'
    )


@pytest.fixture
def test_receiptlines():
    line1 = models.Receiptline(receipt_id='RECEIPT_1', linenumber=1, product_id='PRODUCT_1', amount=1.15)
    line2 = models.Receiptline(receipt_id='RECEIPT_1', linenumber=2, product_id='PRODUCT_1', amount=1.15)
    return [line1, line2]
    

@pytest.fixture
def load_test_data(test_chain, test_store, test_paymentmethod, test_receipt, test_product, test_receiptlines):
    return [test_chain, test_store, test_paymentmethod, test_receipt, test_product, *test_receiptlines]


@pytest.fixture
def test_db_session(load_test_data):
    SessionLocal = sessionmaker(bind=engine)

    session=SessionLocal()

    # I have no idea why this works and session.add_all(load_test_data) didn't
    for obj in load_test_data:
        session.add(obj)
        session.flush()

    yield session

    # drop all data after each test
    for tbl in reversed(Base.metadata.sorted_tables):
        engine.execute(tbl.delete())
    
    session.close()


@pytest.fixture(autouse=True)
def client():
    with TestClient(app) as c:
        yield c
