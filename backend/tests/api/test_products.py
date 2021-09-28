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


def test_put_new(client):
    product_in = {'id': 'NEWPRODUCT', 'name': 'A new product'}

    response = client.put(f"/products/{product_in['id']}", json=product_in)

    assert response.status_code == 201

    data = response.json()

    assert product_in == data


def test_put_existing(client, test_data):
    product_id = test_data['product'].id
    product_in = {'id': product_id, 'name': 'A whole new name'}

    response = client.put(f"/products/{product_in['id']}", json=product_in)

    assert response.status_code == 200

    data = response.json()

    assert product_in == data
