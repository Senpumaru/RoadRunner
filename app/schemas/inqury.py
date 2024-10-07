from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InquiryBase(BaseModel):
    issue_type: str
    description: str

class InquiryCreate(InquiryBase):
    customer_id: int
    product_id: int

class InquiryUpdate(InquiryBase):
    pass

class Inquiry(InquiryBase):
    id: int
    customer_id: int
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True