import pytest


@pytest.mark.parametrize(
    "active_only,expected_count",
    [
        (False, 9),  # All units
        (True, 8),  # Only active units
    ],
)
def test_read_units(test_client, active_only, expected_count):
    # Seed inactive units
    test_client.put(
        "/units/1",
        json={
            "name": "Inactive Unit",
            "name_plural": "Inactive Units",
            "abbr_singular": None,
            "abbr_plural": None,
            "is_active": False,
        },
    )

    # Read units
    response = test_client.get(f"/units/?active_only={str(active_only).lower()}")
    assert response.status_code == 200
    units = response.json()
    assert len(units) == expected_count
    for unit in units:
        if active_only:
            assert unit["is_active"] is True


def test_read_single_unit(test_client):
    # Create a unit
    response = test_client.post(
        "/units/",
        json={
            "name": "Celsius",
            "name_plural": "Celsius",
            "abbr_singular": "C",
            "abbr_plural": "Cs",
        },
    )
    assert response.status_code == 201
    unit_id = response.json()["id"]

    # Fetch the unit
    response = test_client.get(f"/units/{unit_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Celsius"
    assert data["name_plural"] == "Celsius"
    assert data["abbr_singular"] == "C"
    assert data["abbr_plural"] == "Cs"
    assert data["id"] == unit_id


def test_read_nonexistent_unit(test_client):
    response = test_client.get("/units/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_create_unit(test_client):
    response = test_client.post(
        "/units/",
        json={
            "name": "Kilogram",
            "name_plural": "Kilograms",
            "abbr_singular": "kg",
            "abbr_plural": "kgs",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Kilogram"
    assert data["name_plural"] == "Kilograms"
    assert data["abbr_singular"] == "kg"
    assert data["abbr_plural"] == "kgs"
    assert data["is_active"] is True  # Default value for `is_active`


def test_create_duplicate_unit(test_client):
    # Create a unit
    response = test_client.post(
        "/units/",
        json={
            "name": "Gram",
            "name_plural": "Grams",
            "abbr_singular": "g",
            "abbr_plural": "gs",
        },
    )
    assert response.status_code == 201

    # Attempt to create the same unit again
    response = test_client.post(
        "/units/",
        json={
            "name": "Gram",
            "name_plural": "Grams",
            "abbr_singular": "g",
            "abbr_plural": "gs",
        },
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_update_unit(test_client):
    # Create a unit to update
    response = test_client.post(
        "/units/",
        json={
            "name": "Old Unit Name",
            "name_plural": "Old Unit Names",
            "abbr_singular": "OUN",
            "abbr_plural": "OUNs",
        },
    )
    assert response.status_code == 201
    unit_id = response.json()["id"]

    # Update the unit
    response = test_client.put(
        f"/units/{unit_id}",
        json={
            "name": "Updated Unit Name",
            "name_plural": "Updated Unit Names",
            "abbr_singular": "UUN",
            "abbr_plural": "UUNs",
            "is_active": True,
        },
    )
    assert response.status_code == 200
    updated_unit = response.json()
    assert updated_unit["name"] == "Updated Unit Name"
    assert updated_unit["name_plural"] == "Updated Unit Names"
    assert updated_unit["abbr_singular"] == "UUN"
    assert updated_unit["abbr_plural"] == "UUNs"
    assert updated_unit["is_active"] is True


def test_update_unit_conflicting_name(test_client):
    # Create two units
    test_client.post(
        "/units/",
        json={
            "name": "Existing Unit",
            "name_plural": "Existing Units",
            "abbr_singular": "EU",
            "abbr_plural": "EUs",
        },
    )
    response = test_client.post(
        "/units/",
        json={
            "name": "Another Unit",
            "name_plural": "Another Units",
            "abbr_singular": "AU",
            "abbr_plural": "AUs",
        },
    )
    assert response.status_code == 201
    unit_id = response.json()["id"]

    # Attempt to update the second unit with a conflicting name
    response = test_client.put(
        f"/units/{unit_id}",
        json={
            "name": "Existing Unit",
            "name_plural": "Existing Units",
            "abbr_singular": "EU",
            "abbr_plural": "EUs",
            "is_active": True,
        },
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_update_nonexistent_unit(test_client):
    response = test_client.put(
        "/units/99999",
        json={
            "name": "Updated Name",
            "name_plural": "Updated Names",
            "abbr_singular": "UN",
            "abbr_plural": "UNs",
            "is_active": True,
        },
    )
    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"]


def test_delete_unit(test_client):
    # Create a unit to delete
    response = test_client.post(
        "/units/",
        json={
            "name": "To Delete",
            "name_plural": "To Deletes",
            "abbr_singular": "TD",
            "abbr_plural": "TDs",
        },
    )
    assert response.status_code == 201
    unit_id = response.json()["id"]

    # Delete the unit
    response = test_client.delete(f"/units/{unit_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is False


def test_delete_unit_nonexistent_id(test_client):
    response = test_client.delete("/units/99999")
    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"]


def test_delete_unit_invalid_id(test_client):
    response = test_client.delete("/units/blah")
    assert response.status_code == 422
