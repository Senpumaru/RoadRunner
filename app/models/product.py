# app/models/product.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.associations import product_category_association

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    brand = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    categories = relationship("Category", secondary=product_category_association, back_populates="products")
    inquiries = relationship("Inquiry", back_populates="product")