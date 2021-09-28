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

    assert pytest.approx(data1['amount'], test_line1.amount)
    assert pytest.approx(data2['amount'], test_line2.amount)


def test_post(client, test_data):
    receipt_id = test_data['receipt'].id
    product_id = test_data['product'].id

    receiptline_in = {'receipt_id': receipt_id, 'linenumber': 3, 'product_id': product_id, 'amount': 1.11}

    response = client.post(f'/receipts/{receipt_id}/lines', json=receiptline_in)

    assert response.status_code == 201

    data = response.json()

    assert data == receiptline_in
