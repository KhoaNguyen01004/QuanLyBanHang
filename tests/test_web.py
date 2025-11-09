import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestWebRoutes(unittest.TestCase):
    def test_login_page(self):
        response = client.get("/login")
        self.assertIn(response.status_code, [200, 307, 302])

    def test_register_page(self):
        response = client.get("/register")
        self.assertIn(response.status_code, [200, 307, 302])

    def test_home_page(self):
        response = client.get("/")
        self.assertIn(response.status_code, [200, 307, 302])

    def test_cart_page(self):
        response = client.get("/cart")
        self.assertIn(response.status_code, [200, 307, 302, 401])  # 401 if not logged in

    def test_checkout_page(self):
        response = client.get("/checkout")
        self.assertIn(response.status_code, [200, 307, 302])

    def test_logout(self):
        response = client.get("/logout")
        self.assertIn(response.status_code, [200, 307, 302])

if __name__ == '__main__':
    unittest.main()
