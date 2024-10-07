from pydantic import BaseModel
from datetime import datetime
from typing import List

class InquiryBase(BaseModel):
    issue_type: str
    description: str

class InquiryCreate(InquiryBase):
    customer_id: int
    product_id: int

class Inquiry(InquiryBase):
    id: int
    customer_id: int
    product_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ResponseBase(BaseModel):
    content: str
    helpful: bool = None

class ResponseCreate(ResponseBase):
    inquiry_id: int

class Response(ResponseBase):
    id: int
    inquiry_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class InquiryWithResponses(Inquiry):
    responses: List[Response] = []