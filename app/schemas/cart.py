from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .item import Item


class CartItemBase(BaseModel):
    item_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItem(CartItemBase):
    id: int
    cart_id: int
    item: Item

    model_config = ConfigDict(from_attributes=True)


class CartBase(BaseModel):
    user_id: Optional[int] = None
    session_id: Optional[str] = None


class CartCreate(CartBase):
    pass


class Cart(CartBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[CartItem] = []

    model_config = ConfigDict(from_attributes=True)
