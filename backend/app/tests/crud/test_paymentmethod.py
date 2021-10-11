from backend.app import crud, schemas


def test_create_paymentmethod(test_db_session):
    paymentmethod_in = schemas.Paymentmethod(id='CARD', payer='A person')
    db_paymentmethod = crud.paymentmethod.create(test_db_session, obj_in=paymentmethod_in)

    assert db_paymentmethod.id == paymentmethod_in.id
    assert db_paymentmethod.payer == paymentmethod_in.payer


def test_get_paymentmethod(test_data, test_db_session):
    test_paymentmethod = test_data['paymentmethod']
    get_paymentmethod = crud.paymentmethod.get(test_db_session, test_paymentmethod.id)

    assert get_paymentmethod.id == test_paymentmethod.id
    assert get_paymentmethod.payer == test_paymentmethod.payer


def test_update_paymentmethod(test_data, test_db_session):
    test_paymentmethod = test_data['paymentmethod']
    obj_in = schemas.Paymentmethod(id=test_paymentmethod.id, payer='Someone new, perhaps.')

    db_obj = crud.paymentmethod.get(test_db_session, obj_in.id)

    updated_obj = crud.paymentmethod.update(test_db_session, db_obj=db_obj, obj_in=obj_in)

    assert obj_in.id == updated_obj.id
    assert obj_in.payer == updated_obj.payer
