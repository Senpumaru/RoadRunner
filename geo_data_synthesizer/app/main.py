from fastapi import FastAPI
import logging
from app.api.routes import router as api_router
from app.core.config import settings
from app.core.kafka_producer import initialize_kafka_producer, close_kafka_producer, generate_and_send_data_continuously
import asyncio

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    await initialize_kafka_producer()
    asyncio.create_task(generate_and_send_data_continuously())

@app.on_event("shutdown")
async def shutdown_event():
    await close_kafka_producer()