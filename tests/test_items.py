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

class TestItemsAPI(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
