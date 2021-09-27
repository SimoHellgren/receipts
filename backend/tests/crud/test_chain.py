from backend import crud, schemas


def test_create_chain(test_db_session):
    chain_in = schemas.Chain(id='CHAIN_2', name='Chain 2')

    db_chain = crud.create_chain(test_db_session, chain_in)

    assert chain_in.id == db_chain.id
    assert chain_in.name == db_chain.name


def test_get_chain(test_data, test_db_session):
    test_chain = test_data['chain']
    get_chain = crud.get_chain(test_db_session, test_chain.id)

    assert get_chain.id == test_chain.id
    assert get_chain.name == test_chain.name


def test_update_chain(test_data, test_db_session):
    test_chain = test_data['chain']
    new_chain = schemas.Chain(id=test_chain.id, name='New Name!')

    db_chain = crud.update_chain(test_db_session, new_chain)

    assert db_chain.id == new_chain.id
    assert db_chain.name == new_chain.name
