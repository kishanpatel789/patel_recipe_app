import pytest


@pytest.mark.parametrize(
    "active_only,expected_count",
    [
        (False, 9),  # Include both active and inactive tags
        (True, 8),  # Only active tags
    ],
)
def test_read_tags(test_db, test_client, active_only, expected_count):
    # Seed inactive tags 
    test_client.put("/tags/1", json={"name": "Inactive Tag", "is_active": False})

    # Read tags
    response = test_client.get(f"/tags/?active_only={str(active_only).lower()}")
    assert response.status_code == 200
    tags = response.json()
    assert len(tags) == expected_count


def test_read_single_tag(test_db, test_client):
    # Create a tag
    response = test_client.post("/tags/", json={"name": "Single Tag"})
    assert response.status_code == 201
    tag_id = response.json()["id"]

    # Read the tag
    response = test_client.get(f"/tags/{tag_id}")
    assert response.status_code == 200
    tag = response.json()
    assert tag["name"] == "Single Tag"


def test_read_nonexistent_tag(test_db, test_client):
    response = test_client.get("/tags/99999")
    assert response.status_code == 404


def test_create_tag(test_db, test_client):
    # Send a POST request to create a tag
    response = test_client.post("/tags/", json={"name": "Vegetarian"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Vegetarian"


def test_create_duplicate_tag(test_db, test_client):
    # Create a tag
    response = test_client.post("/tags/", json={"name": "Duplicate Tag"})
    assert response.status_code == 201

    # Attempt to create a duplicate
    response = test_client.post("/tags/", json={"name": "Duplicate Tag"})
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_update_tag(test_db, test_client):
    # Create a tag to update
    response = test_client.post("/tags/", json={"name": "Old Tag Name"})
    assert response.status_code == 201
    tag_id = response.json()["id"]

    # Update the tag
    response = test_client.put(
        f"/tags/{tag_id}", json={"name": "Updated Tag Name", "is_active": True}
    )
    assert response.status_code == 200
    updated_tag = response.json()
    assert updated_tag["name"] == "Updated Tag Name"


def test_update_tag_conflicting_name(test_db, test_client):
    # Create two tags
    response1 = test_client.post("/tags/", json={"name": "Existing Tag"})
    assert response1.status_code == 201
    response2 = test_client.post("/tags/", json={"name": "New Tag"})
    assert response2.status_code == 201
    tag_id = response2.json()["id"]

    # Attempt to update the second tag with a conflicting name
    response = test_client.put(
        f"/tags/{tag_id}", json={"name": "Existing Tag", "is_active": True}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_update_nonexistent_tag(test_db, test_client):
    response = test_client.put(
        "/tags/99999", json={"name": "Updated Name", "is_active": True}
    )
    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"]


def test_delete_tag(test_db, test_client):
    # Create a tag to delete
    response = test_client.post("/tags/", json={"name": "To Delete"})
    assert response.status_code == 201
    tag_id = response.json()["id"]

    # Send DELETE request
    response = test_client.delete(f"/tags/{tag_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is False


def test_delete_tag_nonexistent_id(test_db, test_client):
    response = test_client.delete("/tags/40000")
    assert response.status_code == 404


def test_delete_tag_invalid_id(test_db, test_client):
    response = test_client.delete("/tags/blah")
    assert response.status_code == 422
