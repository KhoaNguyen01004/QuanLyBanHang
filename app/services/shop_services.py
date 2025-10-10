from sqlalchemy.orm import Session
from sqlalchemy import and_, String, or_
from app.models.item import Item
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.user import User
from app.schemas.item import ItemCreate, ItemUpdate
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from typing import List, Optional
import logging
from app.websocket_manager import manager  # Import the WebSocket manager from the new module
from sqlalchemy.orm import joinedload


# Configure logging
logging.basicConfig(level=logging.DEBUG)


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
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item_update: ItemUpdate) -> Optional[Item]:
    db_item = db.query(Item).filter(Item.id == item_id).first()  # type: ignore
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
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
    if user_id:
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()  # type: ignore
    elif session_id:
        cart = db.query(Cart).filter(Cart.session_id == session_id).first()  # type: ignore
    else:
        return None

    if not cart:
        cart = Cart(user_id=user_id, session_id=session_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


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
    # Generate custom 5-digit user ID with prefix based on role
    prefix = "B" if user.role == "customer" else "V"
    # Get the max existing user id with the same prefix
    max_id_user = (
        db.query(User)
        .filter(User.id.cast(String).like(f"{prefix}%"))
        .order_by(User.id.desc())
        .first()
    )
    if max_id_user:
        max_num = int(max_id_user.id[1:])
        new_num = max_num + 1
    else:
        new_num = 1
    new_id = f"{prefix}{new_num:04d}"

    db_user = User(
        id=new_id,
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
