def test_get(client):
    response = client.get('/paymentmethods/')

    assert response.status_code == 200
    
    assert len(response.json()) > 0


def test_post(client):
    pm = {'id': 'PayPal', 'payer': None}

    response = client.post('/paymentmethods/', json=pm)

    assert response.status_code == 201

    data = response.json()

    assert data == pm 


def test_put_new(client):
    obj_in = {'id': 'PayPal', 'payer': 'E. Musk'}

    response = client.put(f"/paymentmethods/{obj_in['id']}", json=obj_in)

    assert response.status_code == 201

    data = response.json()

    assert data == obj_in


def test_put_existing(client, test_data):
    obj_in = {'id': test_data['paymentmethod'].id, 'payer': 'E. Musk'}

    response = client.put(f"/paymentmethods/{obj_in['id']}", json=obj_in)

    assert response.status_code == 200

    data = response.json()

    assert data == obj_in
