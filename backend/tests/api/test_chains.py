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


def test_put_change(client, test_data):
    '''Tests for case when PUT changes the chain'''
    chain_id = test_data['chain'].id
    chain = {
        'id': chain_id,
        'name': 'New name!'
    }

    response = client.put(f'/chains/{chain_id}/', json=chain)

    # assert response.status_code == 201
    
    data = response.json()

    assert chain['id'] == data['id']
    assert chain['name'] == data['name']


def test_put_no_change(client, test_data):
    '''Tests for case when PUT does not change the chain'''
    test_chain = test_data['chain']
    chain_id = test_chain.id
    chain = {
        'id': chain_id,
        'name': test_chain.name
    }

    response = client.put(f'/chains/{chain_id}/', json=chain)

    # assert response.status_code == 200
    
    data = response.json()

    assert chain['id'] == data['id']
    assert chain['name'] == data['name']
