from sqlalchemy import Column, Integer, ForeignKey, Table
from app.db.base import Base

product_category_association = Table(
    'product_category_association', 
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

# You can add other association tables here in the future