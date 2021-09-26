import pytest
from backend import crud

def test_create_receipt(chain_test_data, store_test_data, paymentmethod_test_data, receipt_test_data, test_db_session):
    # This setup is getting rather tedious
    chain = crud.create_chain(test_db_session, chain_test_data)
    store = crud.create_store(test_db_session, store_test_data)
    paymentmethod = crud.create_paymentmethod(test_db_session, paymentmethod_test_data)

    receipt_in = receipt_test_data
    db_receipt = crud.create_receipt(test_db_session, receipt_in)

    assert db_receipt.id == receipt_in.id
    assert db_receipt.store_id == receipt_in.store_id
    assert db_receipt.paymentmethod_id == receipt_in.paymentmethod_id
    assert db_receipt.reprint == receipt_in.reprint
    assert db_receipt.etag == receipt_in.etag
    
    # compare timestamps to avoid timezones for now, though should probably do something more elegant
    assert db_receipt.datetime.timestamp() == receipt_in.datetime.timestamp() 
        
    # totals approximately equal, since they are floats. Should change to integer amount of cents
    assert pytest.approx(db_receipt.total, receipt_in.total)
