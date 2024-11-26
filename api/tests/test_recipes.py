import pytest


@pytest.fixture
def sample_recipe():
    """Sample recipe for testing."""
    return {
        "id": 1,
        "name": "Channa Masala",
        "slug": "channa-masala",
        "is_active": True,
    }


@pytest.fixture
def expected_response_keys_recipes():
    """Fixture to provide expected keys and their types."""
    return {
        "name": str,
        "slug": str,
        "id": int,
        "date_created": str,
        "date_modified": type(None),
        "created_by": int,
        "modified_by": type(None),
        "is_active": bool,
    }


@pytest.fixture
def expected_response_keys_recipe_detail():
    """Fixture to provide expected keys and their types."""
    return {
        "name": str,
        "slug": str,
        "id": int,
        "date_created": str,
        "date_modified": type(None),
        "created_by": int,
        "modified_by": type(None),
        "is_active": bool,
        "directions": list,
    }


def test_read_recipes(test_client, expected_response_keys_recipes):
    response = test_client.get("/recipes/")
    first_recipe = response.json()[0]

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for key, value_type in expected_response_keys_recipes.items():
        assert key in first_recipe, f"Key '{key}' is missing in the response"
        assert isinstance(
            first_recipe[key], value_type
        ), f"Key '{key}' is not of type {value_type}"


def test_read_recipe_by_id(
    test_client, sample_recipe, expected_response_keys_recipe_detail
):
    response = test_client.get(f"/recipes/id/{sample_recipe['id']}")
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["id"] == sample_recipe["id"]
    assert response_json["name"] == sample_recipe["name"]
    assert response_json["slug"] == sample_recipe["slug"]
    assert response_json["is_active"] == sample_recipe["is_active"]
    for key, value_type in expected_response_keys_recipe_detail.items():
        assert key in response_json, f"Key '{key}' is missing in the response"
        assert isinstance(
            response_json[key], value_type
        ), f"Key '{key}' is not of type {value_type}"


def test_read_recipe_by_slug(test_client, sample_recipe, expected_response_keys_recipe_detail):
    response = test_client.get(f"/recipes/slug/{sample_recipe['slug']}")
    response_json = response.json()

    assert response_json["id"] == sample_recipe["id"]
    assert response_json["name"] == sample_recipe["name"]
    assert response_json["slug"] == sample_recipe["slug"]
    assert response_json["is_active"] == sample_recipe["is_active"]
    for key, value_type in expected_response_keys_recipe_detail.items():
        assert key in response_json, f"Key '{key}' is missing in the response"
        assert isinstance(
            response_json[key], value_type
        ), f"Key '{key}' is not of type {value_type}"


def test_read_recipe_by_id_not_found(test_client):
    response = test_client.get("/recipes/id/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe '999' not found"


def test_create_recipe(test_client):
    new_recipe = {
        "name": "New Recipe",
        "slug": "new-recipe",
        "directions": [
            {
                "description_": "Step 1",
                "ingredients": [
                    {"quantity": 2.0, "unit_id": 1, "item": "Eggs"},
                ],
            }
        ],
    }
    response = test_client.post("/recipes/", json=new_recipe)

    assert response.status_code == 201
    assert response.json()["name"] == new_recipe["name"]
    assert response.json()["slug"] == new_recipe["slug"]


def test_create_recipe_conflict(test_client):
    conflicting_recipe = {
        "name": "Test Recipe",
        "slug": "test-recipe",
        "directions": [
            {
                "description_": "Step 1",
                "ingredients": [{"quantity": 2.0, "unit_id": 1, "item": "Flour"}],
            }
        ],
    }
    response = test_client.post("/recipes/", json=conflicting_recipe)
    response = test_client.post("/recipes/", json=conflicting_recipe)

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_update_recipe(test_client, sample_recipe):
    updated_recipe = {
        "name": "Updated Recipe",
        "slug": "updated-recipe",
        "is_active": True,
        "directions": [
            {
                "description_": "Updated Step",
                "ingredients": [
                    {"quantity": 3.0, "unit_id": 1, "item": "Milk"},
                ],
            }
        ],
    }
    response = test_client.put(f"/recipes/{sample_recipe['id']}", json=updated_recipe)

    assert response.status_code == 200
    assert response.json()["name"] == updated_recipe["name"]
    assert response.json()["slug"] == updated_recipe["slug"]


def test_delete_recipe(test_client, sample_recipe):
    response = test_client.delete(f"/recipes/{sample_recipe['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == sample_recipe["id"]
    assert not response.json()["is_active"]
