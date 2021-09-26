from backend import crud

def test_create_paymentmethod(paymentmethod_test_data, test_db_session):
    paymentmethod_in = paymentmethod_test_data

    db_paymentmethod = crud.create_paymentmethod(test_db_session, paymentmethod_in)

    assert db_paymentmethod.id == paymentmethod_in.id
    assert db_paymentmethod.payer == paymentmethod_in.payer
