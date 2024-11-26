def test_get_root(test_client):
    response = test_client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"message": "Recipe API is live."}
