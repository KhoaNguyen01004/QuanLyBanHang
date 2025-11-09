from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.db.db import get_db
from app.schemas.order import Order as OrderSchema
from app.services.shop_services import create_order_from_cart, get_orders_for_user, get_order_for_user
from app.api.carts import get_current_user_dep
from app.models.user import User

router = APIRouter()

@router.get('/my', response_model=List[OrderSchema])
def list_my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_dep)):
    return get_orders_for_user(db, current_user.id)

@router.get('/{order_id}', response_model=OrderSchema)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_dep)):
    order = get_order_for_user(db, current_user.id, order_id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    return order

@router.post('/checkout', response_model=OrderSchema)
async def checkout_order(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_dep)):
    order, error = await create_order_from_cart(db, current_user.id)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return order
