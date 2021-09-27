import pytest

from backend import crud, schemas


def test_get_receiptlines(test_data, test_db_session):
    test_receipt = test_data['receipt']
    test_line1 = test_data['line1']
    test_line2 = test_data['line2']

    lines = sorted(crud.get_receiptlines(test_db_session, test_receipt.id), key=lambda x: x.linenumber)

    assert lines[0].linenumber == test_line1.linenumber
    assert lines[0].receipt_id == test_line1.receipt_id
    assert lines[0].product_id == test_line1.product_id
    assert pytest.approx(lines[0].amount, test_line1.amount)

    assert lines[1].linenumber == test_line2.linenumber
    assert lines[1].receipt_id == test_line2.receipt_id
    assert lines[1].product_id == test_line2.product_id
    assert pytest.approx(lines[1].amount, test_line2.amount)

def test_create_receiptlines(test_data, test_db_session):
    test_receipt = test_data['receipt']
    test_product = test_data['product']
    receiptline_in = schemas.ReceiptlineCreate(linenumber=3, product_id=test_product.id, amount=1.11)

    db_receiptline, = crud.create_receiptlines(test_db_session, test_receipt.id, [receiptline_in])

    assert db_receiptline.linenumber == receiptline_in.linenumber
    assert db_receiptline.product_id == receiptline_in.product_id
    assert pytest.approx(db_receiptline.amount, receiptline_in.amount)
    assert db_receiptline.receipt_id == test_receipt.id
