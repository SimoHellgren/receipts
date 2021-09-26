from backend import crud

def test_get_receiptlines(test_receiptlines, test_receipt, test_db_session):
    lines = crud.get_receiptlines(test_db_session, test_receipt.id)

    assert set(lines) == set(test_receiptlines)