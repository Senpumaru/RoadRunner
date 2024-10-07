from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=False, index=True)
    created_at = Column(DateTime)

    inquiries = relationship("Inquiry", back_populates="customer")

    def __repr__(self):
        return f"Customer(id={self.id}, name='{self.name}', email='{self.email}')"