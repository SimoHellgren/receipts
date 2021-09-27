def test_get_all(client):
    response = client.get('/chains/')

    print(response.content)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_post(client):
    chain = {
        'id': 'CHAIN_X',
        'name': 'Chain X'
    }
    
    response = client.post('/chains/', json=chain)

    assert response.status_code == 201

    data = response.json()

    assert chain['id'] == data['id']
    assert chain['name'] == data['name']


def test_put_new(client):
    '''Tests for case when a new Chain gets created by PUT'''
    chain = {'id': 'NEW_CHAIN', 'name': 'A new chain'}

    response = client.put(f"/chains/{chain['id']}/", json=chain)

    assert response.status_code == 201
    
    data = response.json()

    assert chain['id'] == data['id']
    assert chain['name'] == data['name']


def test_put_existing_change(client, test_data):
    '''Tests for case when an existing chain is updated with a new value'''
    test_chain = test_data['chain']
    
    chain = {'id': test_chain.id, 'name': 'A name change!'}

    response = client.put(f"/chains/{chain['id']}/", json=chain)

    assert response.status_code == 200
    
    data = response.json()

    assert chain['id'] == data['id']
    assert chain['name'] == data['name']


def test_put_existing_no_change(client, test_data):
    '''Tests for case when an existing chain is updated with no new values'''
    test_chain = test_data['chain']
    
    chain = {'id': test_chain.id, 'name': test_chain.name}

    response = client.put(f"/chains/{chain['id']}/", json=chain)

    assert response.status_code == 200
    
    data = response.json()

    assert chain['id'] == data['id']
    assert chain['name'] == data['name']
