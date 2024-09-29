# outlier_producer.py

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import random
import time
import json
from kafka import KafkaProducer
import asyncio

app = FastAPI()

# Kafka configuration
KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "iot_data"

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class OutlierConfig(BaseModel):
    device_id: str
    duration: int  # Duration in seconds
    outlier_probability: float = 0.2
    temperature_range: tuple = (-50, 150)  # Normal range is typically -20 to 50

async def generate_outliers(config: OutlierConfig):
    end_time = time.time() + config.duration
    while time.time() < end_time:
        is_outlier = random.random() < config.outlier_probability
        
        if is_outlier:
            temperature = random.uniform(config.temperature_range[0], config.temperature_range[1])
        else:
            temperature = random.uniform(-20, 50)
        
        data = {
            "device_id": config.device_id,
            "timestamp": time.time(),
            "temperature": temperature,
            "humidity": random.uniform(0, 100),
            "pressure": random.uniform(900, 1100),
            "battery_level": random.uniform(0, 100)
        }
        
        producer.send(KAFKA_TOPIC, value=data)
        await asyncio.sleep(0.1)  # Adjust this to control the rate of data generation

@app.post("/generate_outliers")
async def start_outlier_generation(config: OutlierConfig, background_tasks: BackgroundTasks):
    background_tasks.add_task(generate_outliers, config)
    return {"message": f"Started generating outliers for device {config.device_id} for {config.duration} seconds"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)