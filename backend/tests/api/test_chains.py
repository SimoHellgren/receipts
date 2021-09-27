def test_get_all(client):
    response = client.get('/chains/')

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