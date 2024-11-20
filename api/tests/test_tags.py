
def test_create_tag(test_client, override_get_db):
    # Send a POST request to create a tag
    response = test_client.post(
        "/tags/",
        json={"name": "Vegetarian"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Vegetarian"

