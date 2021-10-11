from os import name
from backend.app import crud, schemas


def test_create_product(test_db_session):
    product_in = schemas.ProductCreate(id='PRODUCT_2')

    db_product = crud.product.create(test_db_session, obj_in=product_in)

    assert db_product.id == product_in.id


def test_get_product(test_data, test_db_session):
    test_product = test_data['product']
    get_product = crud.product.get(test_db_session, test_product.id)

    assert get_product.id == test_product.id
    assert get_product.name == test_product.name


def test_update_product(test_data, test_db_session):
    test_product = test_data['product']

    db_obj = crud.product.get(test_db_session, test_product.id)

    obj_in = schemas.Product(id=test_product.id, name='New product name')

    new_obj = crud.product.update(test_db_session, db_obj=db_obj, obj_in=obj_in)

    assert obj_in.id == new_obj.id
    assert obj_in.name == new_obj.name
