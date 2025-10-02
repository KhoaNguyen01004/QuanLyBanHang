from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.db.db import get_db
from app.schemas.cart import Cart, CartItemCreate
from app.services.shop_services import (
    get_cart, get_or_create_cart, add_item_to_cart,
    remove_item_from_cart, update_cart_item_quantity
)

router = APIRouter()


@router.get("/{cart_id}", response_model=Cart)
def read_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = get_cart(db, cart_id=cart_id)
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart


@router.post("/", response_model=Cart)
def create_cart(user_id: Optional[int] = None, session_id: Optional[str] = None, db: Session = Depends(get_db)):
    if not user_id and not session_id:
        raise HTTPException(status_code=400, detail="Either user_id or session_id must be provided")
    cart = get_or_create_cart(db, user_id=user_id, session_id=session_id)
    return cart


@router.post("/{cart_id}/items", response_model=Cart)
def add_item_to_cart_endpoint(cart_id: int, cart_item: CartItemCreate, db: Session = Depends(get_db)):
    # First check if cart exists
    cart = get_cart(db, cart_id=cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    added_item = add_item_to_cart(db, cart_id=cart_id, item_id=cart_item.item_id, quantity=cart_item.quantity)
    if not added_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Return updated cart
    return get_cart(db, cart_id=cart_id)


@router.delete("/{cart_id}/items/{item_id}")
def remove_item_from_cart_endpoint(cart_id: int, item_id: int, db: Session = Depends(get_db)):
    success = remove_item_from_cart(db, cart_id=cart_id, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart successfully"}


@router.put("/{cart_id}/items/{item_id}")
def update_cart_item_quantity_endpoint(cart_id: int, item_id: int, quantity: int, db: Session = Depends(get_db)):
    if quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")

    updated_item = update_cart_item_quantity(db, cart_id=cart_id, item_id=item_id, quantity=quantity)
    if not updated_item and quantity > 0:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Cart item updated successfully"}
