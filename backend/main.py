from fastapi import FastAPI
import logging
from backend.api.routes import router as api_router
from backend.core.config import settings
from backend.core.kafka_producer import (
    initialize_kafka_producer,
    close_kafka_producer,
    generate_and_send_data_continuously,
    test_kafka_connection
)
import asyncio

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router)

logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    initialization_success = await initialize_kafka_producer()
    if initialization_success:
        if await test_kafka_connection():
            asyncio.create_task(generate_and_send_data_continuously())
        else:
            logger.error("Failed to establish Kafka connection. Data generation task not started.")
    else:
        logger.error("Failed to initialize Kafka producer. Application may not function correctly.")

@app.get("/")
async def root():
    return {"message": "Hello from RoadRunner Synthesizer"}

@app.get("/health")
async def health_check():
    kafka_connected = await test_kafka_connection()
    if kafka_connected:
        return {"status": "healthy", "kafka_connection": "established"}
    else:
        return {"status": "unhealthy", "kafka_connection": "failed"}