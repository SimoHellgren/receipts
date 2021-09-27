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