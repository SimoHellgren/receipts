import pytest
from sqlalchemy.exc import IntegrityError

from backend import crud, schemas


def test_create_store(test_chain, test_db_session):
    store_in = schemas.StoreCreate(id='STORE_2', name='Store 2', chain_id=test_chain.id)
    db_store = crud.create_store(test_db_session, store_in)

    assert db_store.id == store_in.id
    assert db_store.name == store_in.name
    assert db_store.chain_id == store_in.chain_id


def test_create_store_fk_fail(test_db_session):
    '''Store with a non-existing chain_id shan't be created'''
    store_in = schemas.StoreCreate(id='STORE_X', name='Store X', chain_id='UNKNOWN')
    
    with pytest.raises(IntegrityError):
        db_store = crud.create_store(test_db_session, store_in)


def test_get_store(test_store, test_db_session):
    get_store = crud.get_store(test_db_session, test_store.id)

    assert get_store == test_store
