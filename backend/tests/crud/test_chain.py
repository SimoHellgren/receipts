from backend import crud, schemas


def test_create_chain(test_db_session):
    chain_in = schemas.Chain(id='CHAIN_2', name='Chain 2')

    db_chain = crud.create_chain(test_db_session, chain_in)

    assert chain_in.id == db_chain.id
    assert chain_in.name == db_chain.name


def test_get_chain(test_chain, test_db_session):
    get_chain = crud.get_chain(test_db_session, test_chain.id)

    assert get_chain == test_chain
