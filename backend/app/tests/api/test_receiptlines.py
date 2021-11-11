import pytest

def test_get(client, test_data):
    receipt_id = test_data['receipt'].id
    test_line1 = test_data['line1'] 
    test_line2 = test_data['line2']

    response = client.get(f'/receipts/{receipt_id}/lines')

    assert response.status_code == 200

    data1, data2 = sorted(response.json(), key=lambda x: x['linenumber'])

    assert data1['receipt_id'] == data2['receipt_id'] == receipt_id

    assert data1['linenumber'] == test_line1.linenumber
    assert data2['linenumber'] == test_line2.linenumber

    assert data1['product_id'] == test_line1.product_id
    assert data2['product_id'] == test_line2.product_id

    assert data1['amount'] - test_line1.amount == pytest.approx(0)
    assert data2['amount'] - test_line2.amount == pytest.approx(0)


def test_post(client, test_data):
    receipt_id = test_data['receipt'].id
    product_id = test_data['product'].id

    receiptline_in = {'receipt_id': receipt_id, 'linenumber': 3, 'product_id': product_id, 'amount': 1.11}

    response = client.post(f'/receipts/{receipt_id}/lines', json=receiptline_in)

    assert response.status_code == 201

    data = response.json()

    assert data == receiptline_in


def test_put_new_for_receipt(client, test_data):
    receipt_id = test_data['receipt'].id
    product_id = test_data['product'].id
    linenumber = 3

    receiptline_in = {'receipt_id': receipt_id, 'linenumber': linenumber, 'product_id': product_id, 'amount': 1.11}

    response = client.put(f'/receipts/{receipt_id}/lines/{linenumber}', json=receiptline_in)

    assert response.status_code == 201

    data = response.json()

    assert data == receiptline_in


def test_put_existing_for_receipt(client, test_data):
    test_line = test_data['line1']
    receipt_id = test_line.receipt_id
    product_id = test_line.product_id
    linenumber = test_line.linenumber

    receiptline_in = {'receipt_id': receipt_id, 'linenumber': linenumber, 'product_id': product_id, 'amount': 100.11}

    response = client.put(f'/receipts/{receipt_id}/lines/{linenumber}', json=receiptline_in)

    assert response.status_code == 200

    data = response.json()

    assert data == receiptline_in


def test_post_float_price_fails(client, test_data):
    receipt_id = test_data['receipt'].id
    product_id = test_data['product'].id
    linenumber = 3

    receiptline_in = {'receipt_id': receipt_id, 'linenumber': linenumber, 'product_id': product_id, 'amount': 100.11}

    response = client.post(f'/receipts/{receipt_id}/lines', json=receiptline_in)

    assert response.status_code == 422


def test_put_float_price_fails(client, test_data):
    receipt_id = test_data['receipt'].id
    product_id = test_data['product'].id
    linenumber = 3

    receiptline_in = {'receipt_id': receipt_id, 'linenumber': linenumber, 'product_id': product_id, 'amount': 100.11}

    response = client.put(f'/receipts/{receipt_id}/lines/{linenumber}', json=receiptline_in)

    assert response.status_code == 422
