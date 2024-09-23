from fastapi import APIRouter
from backend.models.iot_data_generator import IoTDataGenerator
from backend.core.iot_kafka_producer import send_to_kafka

router = APIRouter()
generator = IoTDataGenerator()

@router.get("/")
async def root():
    return {"message": "Hello from Road Runner Geo Data Synthesizer"}

@router.get("/generate")
async def generate_data():
    data = generator.get_json_data()
    send_to_kafka('geo_data', data)
    return {"message": "Data generated and sent to Kafka", "data": data}
    