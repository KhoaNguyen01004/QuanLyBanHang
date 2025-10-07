from sqlalchemy.orm import Session
from sqlalchemy import and_, String
from app.models.item import Item
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.user import User
from app.schemas.item import ItemCreate, ItemUpdate
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from typing import List, Optional


# Item services
def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()  # type: ignore


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    return db.query(Item).offset(skip).limit(limit).all()  # type: ignore


def create_item(db: Session, item: ItemCreate) -> Item:
    db_item = Item(**item.model_dump())
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
    return db.query(Cart).filter(Cart.id == cart_id).first()  # type: ignore


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


def add_item_to_cart(db: Session, cart_id: int, item_id: int, quantity: int = 1) -> Optional[CartItem]:
    # Check if item exists
    item = db.query(Item).filter(Item.id == item_id).first()  # type: ignore
    if not item:
        return None

    # Check if cart item already exists
    cart_item = db.query(CartItem).filter(
        and_(CartItem.cart_id == cart_id, CartItem.item_id == item_id)  # type: ignore
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart_id, item_id=item_id, quantity=quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item


def remove_item_from_cart(db: Session, cart_id: int, item_id: int) -> bool:
    cart_item = db.query(CartItem).filter(
        and_(CartItem.cart_id == cart_id, CartItem.item_id == item_id)  # type: ignore
    ).first()

    if cart_item:
        db.delete(cart_item)
        db.commit()
        return True
    return False


def update_cart_item_quantity(db: Session, cart_id: int, item_id: int, quantity: int) -> Optional[CartItem]:
    cart_item = db.query(CartItem).filter(
        and_(CartItem.cart_id == cart_id, CartItem.item_id == item_id)  # type: ignore
    ).first()

    if cart_item:
        if quantity <= 0:
            db.delete(cart_item)
        else:
            cart_item.quantity = quantity
        db.commit()
        if quantity > 0:
            db.refresh(cart_item)
            return cart_item
    return None


# User services (basic)
def get_user(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()  # type: ignore


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()  # type: ignore


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
