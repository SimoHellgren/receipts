from backend import crud

def test_no_receipts_in_db(test_db_session):
    '''Ensure there are no receipts to begin with'''
    data = crud.get_receipts(test_db_session)

    assert len(data) == 0
