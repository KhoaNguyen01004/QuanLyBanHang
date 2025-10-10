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

# Recreate schema to ensure it's up-to-date with models
# Base.metadata.drop_all(bind=engine)  # Commented out for safety on real DB
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()  # type: ignore

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def authenticate():
    # Register user
    client.post(
        "/api/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    # API login to get token
    response = client.post(
        "/api/users/token",
        data={"username": "testuser", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print('Login response status:', response.status_code)
    print('Login response text:', response.text)
    try:
        token = response.json().get("access_token")
        print('Access token:', token)
    except Exception as e:
        print("Failed to parse JSON from token response. Status:", response.status_code)
        print("Response text:", response.text)
        raise e
    return {"Authorization": f"Bearer {token}"}

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

class TestShopAPI(unittest.TestCase):

    def setUp(self):
        # Create tables
        Base.metadata.create_all(bind=engine)

    def tearDown(self):
        # Clean up all test data after each test
        truncate_tables(engine)

    def test_create_item(self):
        response = client.post(
            "/api/items/",
            json={"name": "Test Item", "price": 10.99, "description": "A test item"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test Item")
        self.assertEqual(data["price"], 10.99)

    def test_read_items(self):
        # Create an item first
        client.post(
            "/api/items/",
            json={"name": "Test Item", "price": 10.99}
        )

        response = client.get("/api/items/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data), 0)

    def test_read_item(self):
        # Create an item first
        create_response = client.post(
            "/api/items/",
            json={"name": "Test Item", "price": 10.99}
        )
        item_id = create_response.json()["id"]

        response = client.get(f"/api/items/{item_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test Item")

    def test_update_item(self):
        # Create an item first
        create_response = client.post(
            "/api/items/",
            json={"name": "Test Item", "price": 10.99}
        )
        item_id = create_response.json()["id"]

        response = client.put(
            f"/api/items/{item_id}",
            json={"name": "Updated Item", "price": 15.99}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Updated Item")
        self.assertEqual(data["price"], 15.99)

    def test_delete_item(self):
        # Create an item first
        create_response = client.post(
            "/api/items/",
            json={"name": "Test Item", "price": 10.99}
        )
        item_id = create_response.json()["id"]

        response = client.delete(f"/api/items/{item_id}")
        self.assertEqual(response.status_code, 200)

        # Try to get the deleted item
        get_response = client.get(f"/api/items/{item_id}")
        self.assertEqual(get_response.status_code, 404)

    def test_create_cart(self):
        response = client.post("/api/carts/?session_id=test_session")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data["id"])

    def test_add_item_to_cart(self):
        headers = authenticate()
        # Create an item
        item_response = client.post(
            "/api/items/",
            json={"name": "Cart Item", "price": 5.99},
            headers=headers
        )
        item_id = item_response.json()["id"]

        # Create a cart
        cart_response = client.post("/api/carts/?session_id=test_session", headers=headers)
        cart_id = cart_response.json()["id"]

        # Add item to cart
        response = client.post(
            f"/api/carts/{cart_id}/items",
            json={"item_id": item_id, "quantity": 2},
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["quantity"], 2)

    def test_create_user(self):
        response = client.post(
            "/api/users/",
            json={"username": "testuser", "email": "test@example.com", "password": "password123"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "test@example.com")

    def test_health_check(self):
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")


if __name__ == '__main__':
    unittest.main()
