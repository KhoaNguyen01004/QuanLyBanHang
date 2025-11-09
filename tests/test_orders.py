import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestOrdersAPI(unittest.TestCase):
    def authenticate(self):
        client.post('/api/users/', json={'username':'buyer','email':'buyer@example.com','password':'secret123'})
        resp = client.post('/api/users/token', data={'username':'buyer','password':'secret123'}, headers={'Content-Type':'application/x-www-form-urlencoded'})
        token = resp.json().get('access_token')
        return {'Authorization': f'Bearer {token}'}

    def test_checkout_flow(self):
        headers = self.authenticate()
        # create item
        item_resp = client.post('/api/items/', json={'name':'Purchased Item','price':10.0,'stock':50}, headers=headers)
        item_id = item_resp.json()['id']
        # create cart and add item
        user_id = 'buyer'  # matches username used in authentication
        cart_resp = client.post(f'/api/carts/?user_id={user_id}', headers=headers)
        cart_id = cart_resp.json()['id']
        client.post(f'/api/carts/{cart_id}/items', json={'item_id': item_id, 'quantity': 3}, headers=headers)
        # DEBUG: fetch cart contents before checkout
        cart_detail = client.get(f'/api/carts/{cart_id}', headers=headers).json()
        print('Cart before checkout:', cart_detail)
        # perform checkout
        order_resp = client.post('/api/orders/checkout', headers=headers)
        self.assertEqual(order_resp.status_code, 200, order_resp.text)
        order = order_resp.json()
        self.assertEqual(order['total_amount'], 30.0)
        self.assertEqual(len(order['items']), 1)
        self.assertEqual(order['items'][0]['quantity'], 3)
        # orders list
        list_resp = client.get('/api/orders/my', headers=headers)
        self.assertEqual(list_resp.status_code, 200)
        self.assertTrue(any(o['id'] == order['id'] for o in list_resp.json()))

if __name__ == '__main__':
    unittest.main()
