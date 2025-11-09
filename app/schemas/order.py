from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime
from .item import Item

class OrderItemBase(BaseModel):
    item_id: int
    quantity: int
    unit_price: float

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    item: Item
    model_config = ConfigDict(from_attributes=True)

class Order(BaseModel):
    id: int
    user_id: str
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime | None = None
    items: List[OrderItem] = []
    model_config = ConfigDict(from_attributes=True)

