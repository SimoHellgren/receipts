import os

from dotenv import load_dotenv
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from fastapi.testclient import TestClient

from backend.api import app
from backend.models import Base
from backend.dependencies import get_db

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
