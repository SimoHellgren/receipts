from backend import crud

def test_get_product(test_product, test_db_session):
    get_product = crud.get_product(test_db_session, test_product.id)

    assert get_product == test_product