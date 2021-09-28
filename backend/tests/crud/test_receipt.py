from datetime import datetime

import pytest

from backend import crud, schemas


def test_get_receipt(test_data, test_db_session):
    test_receipt = test_data['receipt']
    get_receipt = crud.receipt.get(test_db_session, test_receipt.id)

    assert get_receipt.id == test_receipt.id
    assert get_receipt.store_id == test_receipt.store_id
    assert get_receipt.paymentmethod_id == test_receipt.paymentmethod_id
    assert get_receipt.etag == test_receipt.etag
    assert get_receipt.reprint == test_receipt.reprint

    assert get_receipt.datetime.timestamp() == test_receipt.datetime.timestamp()
    
    assert pytest.approx(get_receipt.total, test_receipt.total)


def test_create_receipt(test_data, test_db_session):
    test_store = test_data['store']
    test_paymentmethod = test_data['paymentmethod']
    
    receipt_in = schemas.ReceiptCreate(
        id='test_receipt',
        datetime=datetime(2021, 1, 1, 0, 0, 0, 0),
        store_id=test_store.id,
        paymentmethod_id=test_paymentmethod.id,
        total=123.123,
        reprint='Välkommen åter!',
        etag='Q29uZ3JhdGlvbiwgeW91IGRvbmUgaXQh'
    )
    db_receipt = crud.receipt.create(test_db_session, obj_in=receipt_in)

    assert db_receipt.id == receipt_in.id
    assert db_receipt.store_id == receipt_in.store_id
    assert db_receipt.paymentmethod_id == receipt_in.paymentmethod_id
    assert db_receipt.reprint == receipt_in.reprint
    assert db_receipt.etag == receipt_in.etag
    
    # compare timestamps to avoid timezones for now, though should probably do something more elegant
    assert db_receipt.datetime.timestamp() == receipt_in.datetime.timestamp() 
        
    # totals approximately equal, since they are floats. Should change to integer amount of cents
    assert pytest.approx(db_receipt.total, receipt_in.total)
