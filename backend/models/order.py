from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)

class OrderCreate(BaseModel):
    items: List[OrderItem]
    total_amount: float = Field(..., gt=0)
    shipping_address: str = Field(..., min_length=1)

class OrderUpdate(BaseModel):
    status: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    shipping_address: str
    created_at: datetime

    class Config:
        from_attributes = True

class OrderListResponse(BaseModel):
    orders: list[OrderResponse]
    pagination: dict
