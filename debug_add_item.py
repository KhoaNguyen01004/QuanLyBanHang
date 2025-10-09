from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.db import Base, get_db
from app.models.item import Item

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Recreate schema
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

print('Creating item...')
item_response = client.post('/api/items/', json={'name': 'Cart Item', 'price': 5.99})
print('item status:', item_response.status_code)
print('item body:', item_response.text)

item_id = None
try:
    item_id = item_response.json().get('id')
except Exception as e:
    print('Failed to parse JSON:', e)

# Check stock in DB
db = TestingSessionLocal()
item_in_db = db.query(Item).filter(Item.id == item_id).first()
print('Item stock in DB:', item_in_db.stock if item_in_db else 'None')
db.close()

print('\nCreating cart...')
cart_response = client.post('/api/carts/?session_id=test_session')
print('cart status:', cart_response.status_code)
print('cart body:', cart_response.text)

cart_id = None
try:
    cart_id = cart_response.json().get('id')
except Exception as e:
    print('Failed to parse JSON:', e)

print('\nAdding item to cart...')
add_response = client.post(f'/api/carts/{cart_id}/items', json={'item_id': item_id, 'quantity': 2})
print('add status:', add_response.status_code)
print('add body:', add_response.text)
