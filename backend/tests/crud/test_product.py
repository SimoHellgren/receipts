from backend import crud, schemas


def test_create_product(test_db_session):
    product_in = schemas.ProductCreate(id='PRODUCT_2')

    db_product = crud.create_product(test_db_session, product_in)

    assert db_product.id == product_in.id


def test_get_product(test_product, test_db_session):
    get_product = crud.get_product(test_db_session, test_product.id)

    assert get_product == test_product
