
def test_create_tag(test_db, test_client):
    # Send a POST request to create a tag
    response = test_client.post(
        "/tags/",
        json={"name": "Vegetarian"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Vegetarian"

