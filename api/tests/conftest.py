# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy.orm import sessionmaker
# from ..main import app
# from ..database import get_db, create_test_engine
# from ..models import metadata_obj

# # create test database engine and session
# TestEngine = create_test_engine()
# TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestEngine)

# @pytest.fixture()
# def test_db():
#     """
#     Set up, create session, and tear down test database
#     """
#     metadata_obj.create_all(bind=TestEngine)
#     try:
#         # yield sessionmaker for tests
#         yield TestSessionLocal
#     finally:
#         metadata_obj.drop_all(bind=TestEngine)

# # Override the get_db dependency to use the test database
# @pytest.fixture()
# def override_get_db(test_db):
#     """
#     Override `get_db` dependency to use test database
#     """
#     def _override_get_db():
#         print("Overriding get_db dependency")
#         db = test_db()
#         try:
#             yield db
#         finally:
#             db.close()

#     app.dependency_overrides[get_db] = _override_get_db
#     yield
#     app.dependency_overrides.clear()

# @pytest.fixture()
# def test_client():
#     with TestClient(app) as client:
#         yield client
