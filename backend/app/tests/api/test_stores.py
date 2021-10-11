def test_get_all(client):
    response = client.get('/stores/')

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_one(client, test_data):
    test_store = test_data['store']

    response = client.get(f'/stores/{test_store.id}/')

    assert response.status_code == 200

    data = response.json()

    assert data['id'] == test_store.id
    assert data['name'] == test_store.name
    assert data['chain_id'] == test_store.chain_id


def test_post(client):
    store_in = {'id': 'NEWSTORE', 'name': 'New Store!', 'chain_id': 'CHAIN_1'}

    response = client.post('/stores/', json=store_in)

    assert response.status_code == 201

    data = response.json()

    assert data == store_in


def test_put_new(client):
    store = {'id': 'NEWSTORE', 'name': 'A new store', 'chain_id': 'CHAIN_1'}

    response = client.put(f"/stores/{store['id']}", json=store)

    assert response.status_code == 201

    data = response.json()

    assert data == store


def test_put_existing(client, test_data):
    test_store = test_data['store']
    store = {'id': test_store.id, 'name': 'A new store', 'chain_id': 'CHAIN_1'}

    response = client.put(f"/stores/{store['id']}", json=store)

    assert response.status_code == 200

    data = response.json()

    assert data == store
