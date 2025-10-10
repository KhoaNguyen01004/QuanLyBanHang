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

class TestCartsAPI(unittest.TestCase):

    def setUp(self):
        # Create tables
        Base.metadata.create_all(bind=engine)

    def tearDown(self):
        # Clean up all test data after each test
        truncate_tables(engine)

    def authenticate(self):
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

    def test_create_cart(self):
        response = client.post("/api/carts/?session_id=test_session")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data["id"])

    def test_add_item_to_cart(self):
        headers = self.authenticate()
        item_response = client.post(
            "/api/items/",
            json={"name": "Cart Item", "price": 5.99},
            headers=headers
        )
        item_id = item_response.json()["id"]
        cart_response = client.post("/api/carts/?session_id=test_session", headers=headers)
        cart_id = cart_response.json()["id"]
        response = client.post(f"/api/carts/{cart_id}/items", json={"item_id": item_id, "quantity": 2}, headers=headers)
        self.assertIn(response.status_code, [200, 201])
        data = response.json()
        self.assertEqual(data["id"], cart_id)
        # Check that the item is in the cart with correct quantity
        found = False
        for item in data["items"]:
            if item["item_id"] == item_id and item["quantity"] == 2:
                found = True
        self.assertTrue(found)

    def test_remove_item_from_cart(self):
        headers = self.authenticate()
        item_response = client.post("/api/items/", json={"name": "Cart Item", "price": 5.99}, headers=headers)
        item_id = item_response.json()["id"]
        cart_response = client.post("/api/carts/?session_id=test_session", headers=headers)
        cart_id = cart_response.json()["id"]
        client.post(f"/api/carts/{cart_id}/items", json={"item_id": item_id, "quantity": 2}, headers=headers)
        response = client.delete(f"/api/carts/{cart_id}/items/{item_id}?quantity=2", headers=headers)
        if response.status_code != 200:
            print('Remove item response:', response.status_code, response.text)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Check that the item is no longer in the cart
        for item in data["items"]:
            self.assertNotEqual(item["item_id"], item_id)

    def test_update_item_quantity_in_cart(self):
        headers = self.authenticate()
        item_response = client.post("/api/items/", json={"name": "Cart Item", "price": 5.99}, headers=headers)
        item_id = item_response.json()["id"]
        cart_response = client.post("/api/carts/?session_id=test_session", headers=headers)
        cart_id = cart_response.json()["id"]
        client.post(f"/api/carts/{cart_id}/items", json={"item_id": item_id, "quantity": 2}, headers=headers)
        response = client.put(f"/api/carts/{cart_id}/items/{item_id}?quantity=5", headers=headers)
        if response.status_code != 200:
            print('Update item quantity response:', response.status_code, response.text)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Check that the item quantity is updated
        found = False
        for item in data["items"]:
            if item["item_id"] == item_id and item["quantity"] == 5:
                found = True
        self.assertTrue(found)

    def test_get_cart_details(self):
        headers = self.authenticate()
        cart_response = client.post("/api/carts/?session_id=test_session", headers=headers)
        cart_id = cart_response.json()["id"]
        response = client.get(f"/api/carts/{cart_id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], cart_id)


if __name__ == '__main__':
    unittest.main()
