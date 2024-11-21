
def test_create_tag(test_db, test_client):
    # Send a POST request to create a tag
    response = test_client.post(
        "/tags/",
        json={"name": "Vegetarian"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Vegetarian"

def test_delete_tag(test_db, test_client):
    response = test_client.delete(
        "/tags/4",
    )
    assert response.status_code == 200
    data = response.json()
    assert data['is_active'] == False

def test_delete_tag_nonexistent_id(test_db, test_client):
    response = test_client.delete(
        "/tags/40000",
    )
    assert response.status_code == 404

def test_delete_tag_invalid_id(test_db, test_client):
    response = test_client.delete(
        "/tags/blah",
    )
    assert response.status_code == 422
