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

class TestCartsAPI(unittest.TestCase):

    def setUp(self):
        # Create tables
        Base.metadata.create_all(bind=engine)

    def tearDown(self):
        # Drop tables
        Base.metadata.drop_all(bind=engine)

    def test_create_cart(self):
        response = client.post("/api/carts/?session_id=test_session")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data["id"])

    def test_add_item_to_cart(self):
        # Create an item
        item_response = client.post(
            "/api/items/",
            json={"name": "Cart Item", "price": 5.99}
        )
        item_id = item_response.json()["id"]

        # Create a cart
        cart_response = client.post("/api/carts/?session_id=test_session")
        cart_id = cart_response.json()["id"]

        # Add item to cart
        response = client.post(
            f"/api/carts/{cart_id}/items",
            json={"item_id": item_id, "quantity": 2}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["quantity"], 2)


if __name__ == '__main__':
    unittest.main()
