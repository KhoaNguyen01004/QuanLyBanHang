import os
import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.db import Base, get_db

# Ensure test.db exists
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'test.db')
if not os.path.exists(TEST_DB_PATH):
    open(TEST_DB_PATH, 'a').close()

# Use SQLite for testing
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

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

def truncate_tables(engine):
    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys=off;"))
        conn.execute(text("BEGIN TRANSACTION;"))
        conn.execute(text("DELETE FROM cart_items;"))
        conn.execute(text("DELETE FROM carts;"))
        conn.execute(text("DELETE FROM items;"))
        conn.execute(text("DELETE FROM users;"))
        conn.execute(text("COMMIT;"))
        conn.execute(text("PRAGMA foreign_keys=on;"))

class TestUsersAPI(unittest.TestCase):

    def setUp(self):
        # Create tables
        Base.metadata.create_all(bind=engine)

    def tearDown(self):
        # Clean up all test data after each test
        truncate_tables(engine)

    def test_create_user(self):
        response = client.post(
            "/api/users/",
            json={"username": "testuser", "email": "test@example.com", "password": "password123"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "test@example.com")

    def test_login_user(self):
        # Register user
        client.post(
            "/api/users/",
            json={"username": "testuser2", "email": "test2@example.com", "password": "password123"}
        )
        # Attempt login with form data (OAuth2PasswordRequestForm expects 'username' and 'password')
        response = client.post(
            "/api/users/token",
            data={"username": "testuser2", "password": "password123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)

    def test_get_user_by_id(self):
        # Register user
        reg = client.post(
            "/api/users/",
            json={"username": "testuser3", "email": "test3@example.com", "password": "password123"}
        )
        user_id = reg.json()["id"]
        # Get user by ID
        response = client.get(f"/api/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], user_id)

    def test_get_user_by_email(self):
        # Register user
        client.post(
            "/api/users/",
            json={"username": "testuser4", "email": "test4@example.com", "password": "password123"}
        )
        # Get user by email
        response = client.get("/api/users/email/test4@example.com")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email"], "test4@example.com")


if __name__ == '__main__':
    unittest.main()
