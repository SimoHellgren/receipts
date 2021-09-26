import pytest

from backend import crud, schemas


def test_get_receiptlines(test_receiptlines, test_receipt, test_db_session):
    lines = crud.get_receiptlines(test_db_session, test_receipt.id)

    assert set(lines) == set(test_receiptlines)


def test_create_receiptlines(test_receipt, test_product, test_db_session):
    receiptline_in = schemas.ReceiptlineCreate(linenumber=3, product_id=test_product.id, amount=1.11)

    db_receiptline, = crud.create_receiptlines(test_db_session, test_receipt.id, [receiptline_in])

    assert db_receiptline.linenumber == receiptline_in.linenumber
    assert db_receiptline.product_id == receiptline_in.product_id
    assert pytest.approx(db_receiptline.amount, receiptline_in.amount)
    assert db_receiptline.receipt_id == test_receipt.id
