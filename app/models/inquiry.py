from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Inquiry(Base):
    __tablename__ = 'inquiries'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    issue_type = Column(String)
    description = Column(String)
    created_at = Column(DateTime)

    customer = relationship("Customer", back_populates="inquiries")
    product = relationship("Product", back_populates="inquiries")
    responses = relationship("Response", back_populates="inquiry")

    def __repr__(self):
        return f"Inquiry(id={self.id}, customer_id={self.customer_id}, product_id={self.product_id}, issue_type='{self.issue_type}')"