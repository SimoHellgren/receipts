from datetime import datetime, timezone

import pytest


def test_get_many(client):
    response = client.get('/receipts/')

    assert response.status_code == 200

    assert len(response.json()) > 0


def test_get_one(client, test_data):
    test_receipt = test_data['receipt']
    
    response = client.get(f'/receipts/{test_receipt.id}')

    assert response.status_code == 200

    data = response.json()
    
    assert data['id'] == test_receipt.id
    assert data['etag'] == test_receipt.etag
    assert data['reprint'] == test_receipt.reprint
    assert data['store_id'] == test_receipt.store_id
    assert data['paymentmethod_id'] == test_receipt.paymentmethod_id
    assert pytest.approx(data['total'], test_receipt.total)
    
    data_timestamp = datetime.strptime(data['datetime'], '%Y-%m-%dT%H:%M:%S%z').timestamp()

    assert data_timestamp == test_receipt.datetime.timestamp()


def test_post(client, test_data):
    test_store = test_data['store']
    test_paymentmethod = test_data['paymentmethod']

    receipt_in = {
        'id': 'test_receipt',
        'datetime': str(datetime(2021, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)),
        'store_id': test_store.id,
        'paymentmethod_id': test_paymentmethod.id,
        'total': 123.123,
        'reprint': 'Välkommen åter!',
        'etag': 'Q29uZ3JhdGlvbiwgeW91IGRvbmUgaXQh'
    }

    response = client.post('/receipts/', json=receipt_in)

    assert response.status_code == 201

    data = response.json()

    data_timestamp = datetime.strptime(data.pop('datetime'), '%Y-%m-%dT%H:%M:%S%z').timestamp()
    receipt_in_timestamp = datetime.strptime(receipt_in.pop('datetime'), '%Y-%m-%d %H:%M:%S%z').timestamp()
    assert data_timestamp == receipt_in_timestamp

    assert data == receipt_in


def test_post_float_total_fails(client, test_data):
    '''We don't want floats flying in, because the DB has integers.'''
    test_store = test_data['store']
    test_paymentmethod = test_data['paymentmethod']
    
    receipt_in = {
        'id': 'test_receipt',
        'datetime': str(datetime(2021, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)),
        'store_id': test_store.id,
        'paymentmethod_id': test_paymentmethod.id,
        'total': 123.123,
        'reprint': 'Välkommen åter!',
        'etag': 'Q29uZ3JhdGlvbiwgeW91IGRvbmUgaXQh'
    }

    response = client.post('/receipts/', json=receipt_in)

    assert response.status_code == 422

def test_put_new(client, test_data):
    test_store = test_data['store']
    test_paymentmethod = test_data['paymentmethod']

    receipt_in = {
        'id': 'test_receipt',
        'datetime': str(datetime(2021, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)),
        'store_id': test_store.id,
        'paymentmethod_id': test_paymentmethod.id,
        'total': 123.123,
        'reprint': 'Välkommen åter!',
        'etag': 'Q29uZ3JhdGlvbiwgeW91IGRvbmUgaXQh'
    }

    response = client.put(f'/receipts/test_receipt', json=receipt_in)

    assert response.status_code == 201

    data = response.json()

    data_timestamp = datetime.strptime(data.pop('datetime'), '%Y-%m-%dT%H:%M:%S%z').timestamp()
    receipt_in_timestamp = datetime.strptime(receipt_in.pop('datetime'), '%Y-%m-%d %H:%M:%S%z').timestamp()
    assert data_timestamp == receipt_in_timestamp

    assert data == receipt_in


def test_put_existing(client, test_data):
    receipt_id = test_data['receipt'].id
    test_store = test_data['store']
    test_paymentmethod = test_data['paymentmethod']

    receipt_in = {
        'id': receipt_id,
        'datetime': str(datetime(2021, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)),
        'store_id': test_store.id,
        'paymentmethod_id': test_paymentmethod.id,
        'total': 123.123,
        'reprint': 'Välkommen åter!',
        'etag': 'Q29uZ3JhdGlvbiwgeW91IGRvbmUgaXQh'
    }

    response = client.put(f'/receipts/{receipt_id}', json=receipt_in)

    assert response.status_code == 200

    data = response.json()

    data_timestamp = datetime.strptime(data.pop('datetime'), '%Y-%m-%dT%H:%M:%S%z').timestamp()
    receipt_in_timestamp = datetime.strptime(receipt_in.pop('datetime'), '%Y-%m-%d %H:%M:%S%z').timestamp()
    assert data_timestamp == receipt_in_timestamp

    assert data == receipt_in
