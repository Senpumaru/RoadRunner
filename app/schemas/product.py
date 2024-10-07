from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class CategoryBase(BaseModel):
    name: str
    description: str = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: str = None
    price: float = Field(..., ge=0)
    stock: int = Field(..., ge=0)
    brand: str

class ProductCreate(ProductBase):
    categories: List[int] = []  # List of category IDs

class ProductUpdate(ProductBase):
    categories: List[int] = []  # List of category IDs

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    categories: List[Category] = []

    class Config:
        orm_mode = True