import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.db import Base, get_db

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()  # type: ignore

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestUsersAPI(unittest.TestCase):

    def setUp(self):
        # Create tables
        Base.metadata.create_all(bind=engine)

    def tearDown(self):
        # Drop tables
        Base.metadata.drop_all(bind=engine)

    def test_create_user(self):
        response = client.post(
            "/api/users/",
            json={"username": "testuser", "email": "test@example.com", "password": "password123"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "test@example.com")


if __name__ == '__main__':
    unittest.main()
