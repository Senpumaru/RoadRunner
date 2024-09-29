# iot_kafka_producer.py

import socket
import logging
import asyncio
import time
from confluent_kafka import Producer
from backend.models.iot_data_generator import IoTDataGenerator
from backend.core.config import settings

logger = logging.getLogger(__name__)

producer = None

async def test_kafka_connection():
    global producer
    if producer is None:
        logger.error("Kafka producer is not initialized!")
        return False
    try:
        metadata = producer.list_topics(timeout=10)
        logger.info(f"Successfully connected to Kafka. Broker(s): {metadata.brokers}")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to Kafka: {str(e)}")
        return False

def delivery_report(err, msg):
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    else:
        logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')

async def initialize_kafka_producer():
    global producer
    try:
        logger.info(f"Attempting to initialize Kafka producer with bootstrap servers: {settings.KAFKA_BOOTSTRAP_SERVERS}")
        kafka_config = {
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'client.id': socket.gethostname() + "_iot"
        }
        producer = Producer(kafka_config)
        logger.info("IoT Kafka producer initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize IoT Kafka producer: {str(e)}")
        return False

async def close_kafka_producer():
    if producer:
        producer.flush()

def send_to_kafka(topic: str, message: str, max_retries=3):
    global producer
    retries = 0
    while retries < max_retries:
        if producer is None:
            logger.error(f"Kafka producer is not initialized! Attempt {retries + 1}/{max_retries}")
            time.sleep(1)
            retries += 1
            continue
        try:
            producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
            producer.poll(0)
            return
        except Exception as e:
            logger.error(f"Failed to send message to Kafka: {str(e)}. Attempt {retries + 1}/{max_retries}")
            retries += 1
            time.sleep(1)
    raise RuntimeError(f"Failed to send message to Kafka after {max_retries} attempts")

# Initialize the generator with a 5% chance of generating outliers
generator = IoTDataGenerator(outlier_probability=0.05)

async def generate_and_send_iot_data_continuously():
    while True:
        if producer is None:
            logger.error("IoT Kafka producer is not initialized. Waiting...")
            await asyncio.sleep(5)
            continue
        data = generator.get_json_data()
        try:
            send_to_kafka('iot_data', data)
            logger.info(f"Sent IoT data to Kafka: {data}")
        except Exception as e:
            logger.error(f"Failed to send IoT data to Kafka: {str(e)}")
        await asyncio.sleep(0.1)