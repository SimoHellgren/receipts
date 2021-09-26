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
from backend import schemas

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


@pytest.fixture(autouse=True)
def test_db_session():
    SessionLocal = sessionmaker(bind=engine)

    session=SessionLocal()

    yield session

    # drop all data after each test
    for tbl in reversed(Base.metadata.sorted_tables):
        engine.execute(tbl.delete())
    
    session.close()


@pytest.fixture(autouse=True)
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def chain_test_data():
    chain1 = schemas.Chain(id='CHAIN_1', name='Chain 1')
    return chain1


@pytest.fixture
def store_test_data():
    store1 = schemas.StoreCreate(id='STORE_1', name='Store 1', chain_id='CHAIN_1')
    return store1


@pytest.fixture
def paymentmethod_test_data():
    paymentmethod1 = schemas.Paymentmethod(id='CASH', payer=None)
    return paymentmethod1


@pytest.fixture
def receipt_test_data():
    receipt1 = schemas.ReceiptCreate(
        datetime=datetime(2021, 1, 1, 0, 0, 0, 0),
        store_id='STORE_1',
        paymentmethod_id='CASH',
        total=11.11,
        id='test_id',
        reprint='Test reprint',
        etag='iuyweriuyweriuyhsdkjhskjfh'
    )

    return receipt1
