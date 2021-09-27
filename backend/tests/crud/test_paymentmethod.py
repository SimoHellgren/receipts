from backend import crud, schemas


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
