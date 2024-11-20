import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from ..main import app
from ..database import get_db, create_test_engine
from ..models import metadata_obj

TestEngine = create_test_engine()
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestEngine)


@pytest.fixture()
def override_get_db():
    # override app dependency
    def _override_get_db():
        print("Overriding get_db dependency")
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture()
def test_client():
    yield TestClient(app)


def test_create_tag(override_get_db, test_client):
    # initialize database
    metadata_obj.create_all(bind=TestEngine)


    # test tag creation
    response = test_client.post(
        "/tags/",
        json={"name": "Vegetarian"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Vegetarian"

    # tear down db
    metadata_obj.drop_all(bind=TestEngine)
