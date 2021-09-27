def test_get(client):
    response = client.get('/products/')

    assert response.status_code == 200

    assert len(response.json()) > 0


def test_post(client):
    product_in = {'id': 'NEWPRODUCT', 'name': None}

    response = client.post('/products/', json=product_in)

    assert response.status_code == 201

    data = response.json()

    assert data == product_in
