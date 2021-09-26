from backend import crud

def test_create_chain(chain_test_data, test_db_session):
    chain_in = chain_test_data

    db_chain = crud.create_chain(test_db_session, chain_in)

    assert chain_in.id == db_chain.id
    assert chain_in.name == db_chain.name