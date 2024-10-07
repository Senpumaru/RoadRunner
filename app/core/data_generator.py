from sqlalchemy.orm import Session
from app.models import Product, Customer, Inquiry, Response, Category
from app.schemas import product, customer, support
from faker import Faker
import random
from sqlalchemy import select
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.customer import Customer as CustomerSchema
from app.schemas.inqury import Inquiry as InquirySchema
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker()

def generate_products(db: Session, count: int):
    categories = [Category(name=fake.word(), description=fake.sentence()) for _ in range(5)]
    db.add_all(categories)
    db.commit()

    products = []
    for _ in range(count):
        product = Product(
            name=fake.text(),
            description=fake.text(),
            price=round(random.uniform(10, 1000), 2),
            stock=random.randint(0, 1000),
            brand=fake.company(),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
            categories=random.sample(categories, random.randint(1, 3))
        )
        products.append(product)

    db.add_all(products)
    db.commit()
    return products

async def generate_customers(db: AsyncSession, count: int):
    customers = []
    for i in range(count):
        customer = Customer(
            name=fake.name(),
            email=fake.email(),
            created_at=fake.date_time_this_year()
        )
        db.add(customer)
        logger.debug(f"Added customer to session: {customer}")

    try:
        await db.commit()
        logger.debug("Committed to database")
        for customer in customers:
            await db.refresh(customer)
            logger.debug(f"After commit and refresh: {customer}")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error committing customers: {str(e)}")
        raise

    pydantic_customers = [CustomerSchema.from_orm(customer) for customer in customers]
    for pydantic_customer in pydantic_customers:
        logger.debug(f"Pydantic customer: {pydantic_customer.dict()}")

    return pydantic_customers

async def generate_inquiries(db: AsyncSession, count: int):
    inquiries = []
    
    # Fetch existing customers and products
    customers = (await db.execute(select(Customer))).scalars().all()
    products = (await db.execute(select(Product))).scalars().all()
    
    if not customers or not products:
        logger.error("No customers or products found in the database.")
        return []

    for i in range(count):
        inquiry = Inquiry(
            customer_id=random.choice(customers).id,
            product_id=random.choice(products).id,
            issue_type=random.choice(["Delivery", "Product", "Payment", "Other"]),
            description=fake.text(),
            created_at=fake.date_time_this_year()
        )
        db.add(inquiry)
        logger.debug(f"Added inquiry to session: {inquiry}")

    try:
        await db.commit()
        logger.debug("Committed inquiries to database")
        # Refresh to get the generated IDs
        for inquiry in inquiries:
            await db.refresh(inquiry)
            logger.debug(f"After commit and refresh: {inquiry}")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error committing inquiries: {str(e)}")
        raise

    pydantic_inquiries = [InquirySchema.from_orm(inquiry) for inquiry in inquiries]
    for pydantic_inquiry in pydantic_inquiries:
        logger.debug(f"Pydantic inquiry: {pydantic_inquiry.dict()}")

    return pydantic_inquiries

def generate_responses(db: Session, count: int):
    inquiries = db.query(Inquiry).all()
    
    responses = []
    for _ in range(count):
        response = Response(
            inquiry_id=random.choice(inquiries).id,
            content=fake.text(),
            created_at=fake.date_time_this_year(),
            helpful=random.choice([True, False, None])
        )
        responses.append(response)

    db.add_all(responses)
    db.commit()
    return responses