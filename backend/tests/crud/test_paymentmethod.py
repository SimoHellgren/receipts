from backend import crud, schemas


def test_create_paymentmethod(test_db_session):
    paymentmethod_in = schemas.Paymentmethod(id='CARD', payer='A person')
    db_paymentmethod = crud.create_paymentmethod(test_db_session, paymentmethod_in)

    assert db_paymentmethod.id == paymentmethod_in.id
    assert db_paymentmethod.payer == paymentmethod_in.payer


def test_get_paymentmethod(test_paymentmethod, test_db_session):
    get_paymentmethod = crud.get_paymentmethod(test_db_session, test_paymentmethod.id)

    assert get_paymentmethod == test_paymentmethod
