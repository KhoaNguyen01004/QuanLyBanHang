from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import Optional
from app.db.db import get_db
from app.schemas.cart import Cart, CartItemCreate
from app.services.shop_services import (
    get_cart, get_or_create_cart, add_item_to_cart,
    remove_item_from_cart, update_cart_item_quantity, remove_all_items_from_cart,
    get_user, get_user_by_username_or_email,
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uuid
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter()


@router.get("/{cart_id}", response_model=Cart)
def read_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = get_cart(db, cart_id=cart_id)
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart


@router.post("/", response_model=Cart)
def create_cart(request: Request, user_id: Optional[str] = None, session_id: Optional[str] = None, db: Session = Depends(get_db)):
    # If frontend provided a user_id, try to resolve it (it may be a username)
    if user_id:
        resolved_user = get_user(db, user_id)
        if not resolved_user:
            # try resolving by username or email
            resolved_user = get_user_by_username_or_email(db, user_id)
        if resolved_user:
            user_id = resolved_user.id
        else:
            # If the provided user_id doesn't map to a real user, drop it so we fall back to session behavior
            user_id = None

    # If frontend did not provide user_id/session_id, try to use server session
    if not user_id and not session_id:
        # If user is logged in, use their username/id stored in session
        sess_user = None
        try:
            sess_user = request.session.get('username')
        except Exception:
            sess_user = None
        if sess_user:
            # The session may store either the internal user ID (e.g. 'B0001') or the username.
            # Try to resolve to the internal user id before using it as a foreign key.
            resolved_user = None
            try:
                # Try treat sess_user as an id first
                resolved_user = get_user(db, sess_user)
            except Exception:
                resolved_user = None
            if not resolved_user:
                # Try lookup by username or email
                resolved_user = get_user_by_username_or_email(db, sess_user)
            if resolved_user:
                user_id = resolved_user.id
            else:
                # Could not resolve the session user to a DB user; fall back to guest session behavior
                user_id = None
        else:
            # ensure there is a session_id in the server session
            try:
                session_id = request.session.get('session_id')
                if not session_id:
                    session_id = uuid.uuid4().hex
                    request.session['session_id'] = session_id
            except Exception:
                # As a fallback generate a session id for this request
                session_id = uuid.uuid4().hex

    if not user_id and not session_id:
        raise HTTPException(status_code=400, detail="Either user_id or session_id must be provided")
    cart = get_or_create_cart(db, user_id=user_id, session_id=session_id)
    if cart is None:
        raise HTTPException(status_code=500, detail="Failed to create or retrieve cart")
    return cart


def get_current_user_dep(request: Request, db: Session = Depends(get_db)):
    # Extract token from Authorization header
    auth_header = request.headers.get("authorization")
    token = None
    if auth_header and auth_header.lower().startswith("bearer "):
        token = auth_header[7:]
    return get_current_user(request, db, token=token)


@router.post("/{cart_id}/items", response_model=Cart)
async def add_item_to_cart_endpoint(
    request: Request,
    cart_id: int,
    cart_item: CartItemCreate,  # <-- must come before Depends!
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dep),
):
    import logging
    logging.warning(f"[CART ENDPOINT] Session content: {dict(request.session) if hasattr(request, 'session') else 'No session'}")
    logging.warning(f"[CART ENDPOINT] Current user: {getattr(current_user, 'username', None)}")
    cart = get_cart(db, cart_id=cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    error = await add_item_to_cart(db, cart_id=cart_id, item_id=cart_item.item_id, quantity=cart_item.quantity)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return get_cart(db, cart_id=cart_id)


@router.delete("/{cart_id}/items/{item_id}")
def remove_item_from_cart_endpoint(
    request: Request,
    cart_id: int,
    item_id: int,
    quantity: int = Query(..., description="Quantity to remove."),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dep),
):
    cart = get_cart(db, cart_id=cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    error = remove_item_from_cart(db, cart_id=cart_id, item_id=item_id, quantity=quantity)
    if error == "Item(s) removed from cart successfully":
        return get_cart(db, cart_id=cart_id)
    elif error:
        raise HTTPException(status_code=400, detail=error)
    return get_cart(db, cart_id=cart_id)


@router.delete("/{cart_id}/items")
def remove_all_items_from_cart_endpoint(cart_id: int, db: Session = Depends(get_db)):
    message = remove_all_items_from_cart(db, cart_id=cart_id)
    return {"message": message}


@router.put("/{cart_id}/items/{item_id}")
def update_cart_item_quantity_endpoint(
    request: Request,
    cart_id: int,
    item_id: int,
    quantity: int = Query(..., description="New quantity for the item."),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dep),
):
    cart = get_cart(db, cart_id=cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    error = update_cart_item_quantity(db, cart_id=cart_id, item_id=item_id, quantity=quantity)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return get_cart(db, cart_id=cart_id)
