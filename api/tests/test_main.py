def test_get_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
