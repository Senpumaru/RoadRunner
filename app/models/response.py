from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Response(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True, index=True)
    inquiry_id = Column(Integer, ForeignKey('inquiries.id'))
    content = Column(String)
    created_at = Column(DateTime)
    helpful = Column(Boolean)

    inquiry = relationship("Inquiry", back_populates="responses")