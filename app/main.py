# main.py

from fastapi import FastAPI
import logging
from app.api.routes import router as api_router
from app.core.config import settings
from app.core.iot_kafka_producer import (
    initialize_kafka_producer,
    close_kafka_producer,
    generate_and_send_iot_data_continuously,
    test_kafka_connection
)
from app.api.endpoints import items, users
from app.core.textual_kafka_producer import (
    initialize_kafka_producer as initialize_textual_producer,
    close_kafka_producer as close_textual_producer,
    generate_and_send_textual_data_continuously,
    test_kafka_connection as test_textual_connection
)
import asyncio

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router)
app.include_router(items.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    return {"message": "Hello from RoadRunner Synthesizer"}

@app.on_event("startup")
async def startup_event():
    iot_init_success = await initialize_kafka_producer()
    textual_init_success = await initialize_textual_producer()
    
    if iot_init_success and textual_init_success:
        iot_connected = await test_kafka_connection()
        textual_connected = await test_textual_connection()
        
        if iot_connected and textual_connected:
            asyncio.create_task(generate_and_send_iot_data_continuously())
            asyncio.create_task(generate_and_send_textual_data_continuously())
        else:
            logger.error("Failed to establish Kafka connection for one or both producers. Data generation tasks not started.")
    else:
        logger.error("Failed to initialize one or both Kafka producers. Application may not function correctly.")

@app.on_event("shutdown")
async def shutdown_event():
    await close_kafka_producer()
    await close_textual_producer()

@app.get("/health")
async def health_check():
    iot_connected = await test_kafka_connection()
    textual_connected = await test_textual_connection()
    if iot_connected and textual_connected:
        return {"status": "healthy", "iot_kafka_connection": "established", "textual_kafka_connection": "established"}
    elif iot_connected:
        return {"status": "partially healthy", "iot_kafka_connection": "established", "textual_kafka_connection": "failed"}
    elif textual_connected:
        return {"status": "partially healthy", "iot_kafka_connection": "failed", "textual_kafka_connection": "established"}
    else:
        return {"status": "unhealthy", "iot_kafka_connection": "failed", "textual_kafka_connection": "failed"}