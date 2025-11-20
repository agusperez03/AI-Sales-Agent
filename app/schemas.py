from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class CartItemBase(BaseModel):
    product_id: int
    qty: int

class CartItem(CartItemBase):
    id: int
    cart_id: int

    class Config:
        orm_mode = True

class CartCreate(BaseModel):
    items: List[CartItemBase]

class CartUpdate(BaseModel):
    items: List[CartItemBase]

class Cart(BaseModel):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    items: List[CartItem] = []

    class Config:
        orm_mode = True
