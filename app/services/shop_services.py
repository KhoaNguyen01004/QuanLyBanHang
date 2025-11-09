from sqlalchemy.orm import Session
from sqlalchemy import and_, String, or_
from app.models.item import Item
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.item import ItemCreate, ItemUpdate
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from typing import List, Optional
import logging
from app.websocket_manager import manager  # Import the WebSocket manager from the new module
from sqlalchemy.orm import joinedload
import re, os


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# New helper: slugify item names for deterministic image filenames
_slug_regex = re.compile(r'[^a-z0-9]+')

def slugify(name: str) -> str:
    if not name:
        return 'item'
    name = name.lower().strip()
    name = _slug_regex.sub('-', name)
    name = re.sub(r'-{2,}', '-', name).strip('-')
    return name or 'item'

# Directory where item images live (relative to static/). We keep this centralized.
ITEM_IMAGE_DIR = os.path.join('static', 'images', 'items')
DEFAULT_IMAGE_REL = 'images/items/default.png'  # relative path used by templates


# Item services
def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()  # type: ignore


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    return db.query(Item).offset(skip).limit(limit).all()  # type: ignore


def create_item(db: Session, item: ItemCreate) -> Item:
    db_item = Item(**item.model_dump())
    # If stock wasn't provided (defaults to None), set a sensible default so items can be added to carts in tests
    if not db_item.stock:
        db_item.stock = 100
    # Auto assign picture_path if missing using slug convention <slug>.png under images/items/
    if not db_item.picture_path:
        slug = slugify(str(db_item.name or ''))
        candidate_rel = f"images/items/{slug}.png"  # path relative to /static
        # If the file actually exists, use it; else keep None (will resolve to default later in view layer)
        if os.path.exists(os.path.join('static', candidate_rel)):
            db_item.picture_path = candidate_rel
        else:
            # Leave as None so frontend can fallback; optionally could set to candidate regardless
            db_item.picture_path = None
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item_update: ItemUpdate) -> Optional[Item]:
    db_item = db.query(Item).filter(Item.id == item_id).first()  # type: ignore
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        name_changed = 'name' in update_data and update_data['name'] and update_data['name'] != db_item.name
        for field, value in update_data.items():
            setattr(db_item, field, value)
        # If name changed and picture_path is empty / None, attempt to set new slug-based path
        if name_changed and not getattr(db_item, 'picture_path', None):
            slug = slugify(str(db_item.name or ''))
            candidate_rel = f"images/items/{slug}.png"
            if os.path.exists(os.path.join('static', candidate_rel)):
                db_item.picture_path = candidate_rel
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> bool:
    db_item = db.query(Item).filter(Item.id == item_id).first()  # type: ignore
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False


# Cart services
def get_cart(db: Session, cart_id: int) -> Optional[Cart]:
    return db.query(Cart).filter(Cart.id == cart_id).options(
        joinedload(Cart.items).joinedload(CartItem.item)  # Eagerly load CartItem and Item relationships
    ).first()  # type: ignore


def get_or_create_cart(db: Session, user_id: Optional[str] = None, session_id: Optional[str] = None) -> Optional[Cart]:
    # Always prefer user_id if present (for authenticated users)
    if user_id:
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()  # type: ignore
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        return cart
    elif session_id:
        cart = db.query(Cart).filter(Cart.session_id == session_id).first()  # type: ignore
        if not cart:
            cart = Cart(session_id=session_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        return cart
    else:
        return None


async def add_item_to_cart(db: Session, cart_id: int, item_id: int, quantity: int = 1) -> Optional[str]:
    # Check if item exists
    item = db.query(Item).filter(Item.id == item_id).first()  # type: ignore
    if not item:
        return "Item not found"
    if item.stock < quantity:
        return "Item is out of stock or not enough stock available"

    # Check if cart item already exists
    cart_item = db.query(CartItem).filter(
        and_(CartItem.cart_id == cart_id, CartItem.item_id == item_id)  # type: ignore
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            cart_id=cart_id,
            item_id=item_id,
            quantity=quantity
        )
        db.add(cart_item)

    # Reduce stock
    item.stock -= quantity
    db.commit()
    db.refresh(cart_item)

    # Notify clients about the stock update
    await manager.broadcast(f"Stock updated: Item {item.id} now has {item.stock} units remaining.")
    await manager.broadcast({"type": "stock_update", "item_id": item.id, "stock": item.stock})

    # Log the broadcast message for debugging
    print(f"Broadcasting stock update: Item {item.id}, Stock {item.stock}")

    return None  # None means success


def remove_item_from_cart(db: Session, cart_id: int, item_id: int, quantity: int = None, remove_all: bool = False) -> str:
    logging.debug(f"Attempting to remove item {item_id} from cart {cart_id} with quantity {quantity} and remove_all={remove_all}")
    cart_item = db.query(CartItem).filter(
        and_(CartItem.cart_id == cart_id, CartItem.item_id == item_id)  # type: ignore
    ).first()
    item = db.query(Item).filter(Item.id == item_id).first()  # type: ignore
    if not cart_item or not item:
        logging.debug("Item not found in cart or item does not exist.")
        return "Item not found in cart"

    if remove_all:
        logging.debug(f"Removing all of item {item_id} from cart {cart_id}.")
        # Restore all stock
        item.stock += cart_item.quantity
        db.delete(cart_item)
    elif quantity is not None and quantity >= cart_item.quantity:
        logging.debug(f"Removing all of item {item_id} from cart {cart_id} due to quantity >= cart_item.quantity.")
        # Restore all stock
        item.stock += cart_item.quantity
        db.delete(cart_item)
    elif quantity is not None:
        logging.debug(f"Reducing quantity of item {item_id} in cart {cart_id} by {quantity}.")
        cart_item.quantity -= quantity
        item.stock += quantity
    else:
        logging.debug("Invalid quantity: None. Cannot proceed with removal.")
        return "Invalid quantity provided"

    db.commit()
    logging.debug("Item(s) removed from cart successfully.")
    return "Item(s) removed from cart successfully"


def remove_all_items_from_cart(db: Session, cart_id: int) -> str:
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()  # type: ignore
    for cart_item in cart_items:
        item = db.query(Item).filter(Item.id == cart_item.item_id).first()  # type: ignore
        if item:
            item.stock += cart_item.quantity
        db.delete(cart_item)
    db.commit()
    return "All items removed from cart successfully"


def update_cart_item_quantity(db: Session, cart_id: int, item_id: int, quantity: int) -> Optional[str]:
    cart_item = db.query(CartItem).filter(
        and_(CartItem.cart_id == cart_id, CartItem.item_id == item_id)
    ).first()
    item = db.query(Item).filter(Item.id == item_id).first()
    if not cart_item or not item:
        return "Item not found in cart"
    diff = quantity - cart_item.quantity
    if diff > 0:
        if item.stock < diff:
            return "Not enough stock"
        item.stock -= diff
    else:
        item.stock += abs(diff)
    if quantity == 0:
        db.delete(cart_item)
    else:
        cart_item.quantity = quantity
    db.commit()
    return None


# User services (basic)
def get_user(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()  # type: ignore


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()  # type: ignore


def get_user_by_username_or_email(db: Session, identifier: str) -> Optional[User]:
    return db.query(User).filter(or_(User.username == identifier, User.email == identifier)).first()  # type: ignore


def create_user(db: Session, user: UserCreate) -> User:
    # Site is customer-only. Use fixed prefix 'B' for customer user IDs.
    prefix = "B"
    # Get the max existing user id with the same prefix
    max_id_user = (
        db.query(User)
        .filter(User.id.cast(String).like(f"{prefix}%"))
        .order_by(User.id.desc())
        .first()
    )
    if max_id_user:
        # Ensure we cast to str in case the ORM returns a ColumnElement; slicing requires a string
        max_num = int(str(max_id_user.id)[1:])
        new_num = max_num + 1
    else:
        new_num = 1
    new_id = f"{prefix}{new_num:04d}"

    db_user = User(
        id=new_id,
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    try:
        db.commit()
    except Exception:
        # Ensure the session is rolled back so subsequent queries in the same request
        # are not executed in an aborted transaction.
        db.rollback()
        raise
    db.refresh(db_user)
    return db_user


def get_orders_for_user(db: Session, user_id: str):
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()


def get_order_for_user(db: Session, user_id: str, order_id: int):
    return db.query(Order).filter(Order.user_id == user_id, Order.id == order_id).first()


async def create_order_from_cart(db: Session, user_id: str):
    # Ensure cart exists and has items
    cart = get_or_create_cart(db, user_id=user_id)
    if not cart or not cart.items:
        return None, 'Cart is empty'
    # Build order
    total = 0.0
    order = Order(user_id=user_id, total_amount=0.0, status='completed')
    db.add(order)
    db.flush()  # get order.id before adding items
    for ci in cart.items:
        item = ci.item
        if not item:
            continue
        unit_price = float(item.price or 0.0)
        quantity = int(ci.quantity or 0)
        line_total = unit_price * quantity
        total += line_total
        oi = OrderItem(order_id=order.id, item_id=item.id, quantity=quantity, unit_price=unit_price)
        db.add(oi)
    order.total_amount = total
    # Clear cart items (stock not restored because already decremented on add)
    for ci in list(cart.items):
        db.delete(ci)
    db.commit()
    db.refresh(order)
    return order, None
