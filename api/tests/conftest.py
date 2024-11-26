import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..database import get_db, create_test_engine
from ..models import metadata_obj
from .seed_test_db import seed_test_db

# create test database engine and session
TestEngine = create_test_engine()
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestEngine)


@pytest.fixture(scope="session")
def test_db():
    """Fixture to initialize a test database and override the fastapi application's db dependency"""
    # initialize database
    metadata_obj.create_all(bind=TestEngine)

    # seed database
    seed_test_db(TestSessionLocal)

    # override app dependency
    def _override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _override_get_db

    yield

    # clear app dependency and tear down db
    app.dependency_overrides.clear()
    metadata_obj.drop_all(bind=TestEngine)


@pytest.fixture(scope="module")
def test_client(test_db):
    """Fixture to generate test client"""
    yield TestClient(app)
