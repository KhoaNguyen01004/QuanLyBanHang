import random
from app.db.db import SessionLocal
from app.models.item import Item
from app.models.cart_item import CartItem
from app.models.cart import Cart
from app.models.user import User  # Ensure all relationships are resolved

# List of new items to insert
new_items = [
    {
        "name": "Wireless Headphones",
        "description": "High-quality wireless headphones with noise cancellation and long battery life. Perfect for music lovers and professionals.",
        "picture_path": "images/items/Screenshot 2025-10-02 215021.png",
        "tags": "electronics,audio,wireless"
    },
    {
        "name": "Smartphone Case",
        "description": "Durable and stylish case for smartphones, providing protection against drops and scratches.",
        "picture_path": "images/items/Screenshot 2025-10-02 215518.png",
        "tags": "accessories,protection,mobile"
    },
    {
        "name": "Laptop Stand",
        "description": "Adjustable laptop stand for better ergonomics and cooling during work sessions.",
        "picture_path": "images/items/Screenshot 2025-10-03 022445.png",
        "tags": "computer,ergonomics,stand"
    },
    {
        "name": "Bluetooth Speaker",
        "description": "Portable Bluetooth speaker with excellent sound quality and waterproof design.",
        "picture_path": "images/items/Screenshot 2025-10-06 102429.png",
        "tags": "audio,portable,bluetooth"
    },
    {
        "name": "Gaming Mouse",
        "description": "Precision gaming mouse with customizable buttons and RGB lighting.",
        "picture_path": "images/items/Screenshot 2025-10-06 102502.png",
        "tags": "computer,accessories,gaming"
    },
    {
        "name": "Mechanical Keyboard",
        "description": "Mechanical keyboard with tactile switches and customizable RGB backlighting.",
        "picture_path": "images/items/Screenshot 2025-10-06 104534.png",
        "tags": "computer,accessories,keyboard"
    },
    {
        "name": "Smartwatch",
        "description": "Feature-rich smartwatch with fitness tracking, notifications, and long battery life.",
        "picture_path": "images/items/Screenshot 2025-10-06 104916.png",
        "tags": "wearable,fitness,smart"
    },
    {
        "name": "Portable SSD",
        "description": "High-speed portable SSD for fast data transfer and secure storage on the go.",
        "picture_path": "images/items/Screenshot 2025-10-06 105734.png",
        "tags": "storage,portable,ssd"
    },
]

def random_price():
    return round(random.uniform(29.99, 399.99), 2)

def random_stock():
    return random.randint(10, 100)

def main():
    db = SessionLocal()
    # Delete all cart items first to avoid foreign key constraint errors
    db.query(CartItem).delete()
    db.commit()
    # Delete all carts (to avoid orphaned carts)
    db.query(Cart).delete()
    db.commit()
    # Delete all existing items
    db.query(Item).delete()
    db.commit()
    # Insert new items
    for item in new_items:
        db_item = Item(
            name=item["name"],
            description=item["description"],
            price=random_price(),
            stock=random_stock(),
            picture_path=item["picture_path"],
            tags=item["tags"]
        )
        db.add(db_item)
    db.commit()
    db.close()
    print("Database populated with 8 real items.")

if __name__ == "__main__":
    main()
