from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Additional fields present in the DB model that the frontend expects
    stock: int = 0
    picture_path: Optional[str] = None
    tags: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('tags', mode='before')
    def _split_tags(cls, v):
        # DB stores tags as a comma-separated string; convert to list for the API
        if v is None:
            return []
        if isinstance(v, str):
            return [t.strip() for t in v.split(',') if t.strip()]
        if isinstance(v, list):
            return v
        return []
