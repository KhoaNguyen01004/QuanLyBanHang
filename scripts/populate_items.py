import os
import sys
import random

# --- Path bootstrap so running this file directly works (python scripts/populate_items.py) ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.db.db import SessionLocal  # noqa: E402
from app.models.item import Item  # noqa: E402
from app.models.cart_item import CartItem  # noqa: E402
from app.models.cart import Cart  # noqa: E402
from app.models.order_item import OrderItem  # noqa: E402
from app.models.order import Order  # noqa: E402
# Note: If you are using relationships that require User metadata during population,
# you can import it here: from app.models.user import User  # noqa: E402

"""Populate the database with a curated set of demo items.
(Updated to safely clear dependent tables in FK order.)

Usage (from project root):
  Windows cmd:   set SECRET_KEY=dev-secret && python -m scripts.populate_items
  Windows PowerShell:  $env:SECRET_KEY='dev-secret'; python -m scripts.populate_items
  Linux/macOS:   SECRET_KEY=dev-secret python -m scripts.populate_items

After this edit you can also run directly:
  python scripts/populate_items.py
"""

# List of new items to insert
new_items = [
    {
        "name": "Wireless Headphones",
        "description": "High-quality wireless headphones with noise cancellation and long battery life. Perfect for music lovers and professionals.",
        "picture_path": "images/items/Wireless_Headphone.png",
        "tags": "electronics,audio,wireless"
    },
    {
        "name": "Smartphone Case",
        "description": "Durable and stylish case for smartphones, providing protection against drops and scratches.",
        "picture_path": "images/items/Smartphone_Case.png",
        "tags": "accessories,protection,mobile"
    },
    {
        "name": "Laptop Stand",
        "description": "Adjustable laptop stand for better ergonomics and cooling during work sessions.",
        "picture_path": "images/items/Laptop_Stand.png",
        "tags": "computer,ergonomics,stand"
    },
    {
        "name": "Bluetooth Speaker",
        "description": "Portable Bluetooth speaker with excellent sound quality and waterproof design.",
        "picture_path": "images/items/Bluetooth_Speaker.png",
        "tags": "audio,portable,bluetooth"
    },
    {
        "name": "Gaming Mouse",
        "description": "Precision gaming mouse with customizable buttons and RGB lighting.",
        "picture_path": "images/items/Gaming_Mouse.png",
        "tags": "gaming,peripheral,mouse"
    },
    {
        "name": "Mechanical Keyboard",
        "description": "Mechanical keyboard with tactile switches for comfortable typing.",
        "picture_path": "images/items/Mechanical_Keyboard.png",
        "tags": "keyboard,mechanical,typing"
    },
    {
        "name": "Smartwatch",
        "description": "Feature-rich smartwatch with fitness tracking, notifications, and long battery life.",
        "picture_path": "images/items/Smartwatch.png",
        "tags": "wearable,fitness,smart"
    },
    {
        "name": "Portable SSD",
        "description": "High-speed portable SSD for fast data transfer and secure storage on the go.",
        "picture_path": "images/items/Portable_SSD.png",
        "tags": "storage,portable,ssd"
    },
]

def random_price():
    return round(random.uniform(29.99, 399.99), 2)

def random_stock():
    return random.randint(10, 100)

def clear_tables(db):
    """Clear dependent tables in proper FK order to avoid violations."""
    # Order: cart_items -> carts -> order_items -> orders -> items
    # (Actually orders/order_items reference items, so we must delete order_items first, then orders, then items.)
    try:
        db.query(CartItem).delete()
        db.commit()
        db.query(Cart).delete()
        db.commit()
        db.query(OrderItem).delete()
        db.commit()
        db.query(Order).delete()
        db.commit()
        db.query(Item).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Failed clearing tables: {e}")
        raise

def insert_items(db):
    for item in new_items:
        db_item = Item(
            name=item["name"],
            description=item["description"],
            price=random_price(),
            stock=random_stock(),
            picture_path=item["picture_path"],
            tags=item["tags"],
        )
        db.add(db_item)
    db.commit()


def main():
    db = SessionLocal()
    try:
        clear_tables(db)
        insert_items(db)
        print("Database populated with 8 real items.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
