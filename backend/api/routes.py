from fastapi import APIRouter
from backend.models.geo_data import GeoDataGenerator
from backend.core.kafka_producer import send_to_kafka

router = APIRouter()
generator = GeoDataGenerator()

@router.get("/")
async def root():
    return {"message": "Hello from Road Runner Geo Data Synthesizer"}

@router.get("/generate")
async def generate_data():
    data = generator.get_json_data()
    send_to_kafka('geo_data', data)
    return {"message": "Data generated and sent to Kafka", "data": data}
    