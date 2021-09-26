from backend import crud


def test_create_store(chain_test_data, store_test_data, test_db_session):
    # create chain due to FK constraints. This should probably be totally restructured in conftest.py,
    # such that we don't always need to separately create all FK-constrained data
    chain_in = chain_test_data
    db_chain = crud.create_chain(test_db_session, chain_in)

    store_in = store_test_data
    db_store = crud.create_store(test_db_session, store_in)

    assert db_store
    assert db_store.id == store_in.id
    assert db_store.name == store_in.name
    assert db_store.chain_id == store_in.chain_id
