from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import product, customer, support
from app.models import Product, Customer, Inquiry, Response, Category
from app.schemas.customer import Customer as CustomerSchema
from app.schemas.inqury import Inquiry as InquirySchema
from app.db.database import get_db
from app.core.data_generator import generate_products, generate_customers, generate_inquiries, generate_responses
from sqlalchemy.ext.asyncio import AsyncSession

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/products", response_model=List[product.Product])
def create_products(count: int, db: Session = Depends(get_db)):
    if count <= 0:
        raise HTTPException(status_code=400, detail="Count must be positive")
    return generate_products(db, count)

@router.post("/customers", response_model=List[CustomerSchema])
async def create_customers(count: int, db: AsyncSession = Depends(get_db)):
    if count <= 0:
        raise HTTPException(status_code=400, detail="Count must be positive")
    customers = await generate_customers(db, count)
    return customers

@router.post("/inquiries", response_model=List[InquirySchema])
async def create_inquiries(count: int, db: AsyncSession = Depends(get_db)):
    if count <= 0:
        raise HTTPException(status_code=400, detail="Count must be positive")
    inquiries = await generate_inquiries(db, count)
    return inquiries

@router.post("/responses", response_model=List[support.Response])
def create_responses(count: int, db: Session = Depends(get_db)):
    if count <= 0:
        raise HTTPException(status_code=400, detail="Count must be positive")
    return generate_responses(db, count)

@router.post("/all")
def generate_all_data(product_count: int, customer_count: int, inquiry_count: int, response_count: int, db: Session = Depends(get_db)):
    if any(count <= 0 for count in [product_count, customer_count, inquiry_count, response_count]):
        raise HTTPException(status_code=400, detail="All counts must be positive")
    
    products = generate_products(db, product_count)
    customers = generate_customers(db, customer_count)
    inquiries = generate_inquiries(db, inquiry_count)
    responses = generate_responses(db, response_count)
    
    return {
        "products": len(products),
        "customers": len(customers),
        "inquiries": len(inquiries),
        "responses": len(responses)
    }