# app/models/__init__.py
from app.db.base import Base
from .user import User
from .item import Item
from .product import Product
from .response import Response
from .category import Category
from .customer import Customer
from .inquiry import Inquiry
from .associations import product_category_association