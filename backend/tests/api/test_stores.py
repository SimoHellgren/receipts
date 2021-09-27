def test_get_all(client):
    response = client.get('/stores/')

    assert response.status_code == 200
    assert len(response.json()) > 0