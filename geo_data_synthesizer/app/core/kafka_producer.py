import socket
import logging
import asyncio
from app.models.geo_data import GeoDataGenerator
from confluent_kafka import Producer
from app.core.config import settings

producer = None
logger = logging.getLogger(__name__)

def delivery_report(err, msg):
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    else:
        logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')

async def initialize_kafka_producer():
    global producer
    logger.info(f"Initializing Kafka producer with bootstrap servers: {settings.KAFKA_BOOTSTRAP_SERVERS}")
    kafka_config = {
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
        'client.id': socket.gethostname()
    }
    try:
        producer = Producer(kafka_config)
        logger.info(f"Kafka producer initialized successfully with config: {kafka_config}")
    except Exception as e:
        logger.error(f"Failed to initialize Kafka producer: {str(e)}")
        raise

async def close_kafka_producer():
    if producer:
        producer.flush()

def delivery_report(err, msg):
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    else:
        logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def send_to_kafka(topic: str, message: str):
    if producer:
        try:
            producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
            producer.poll(0)
        except Exception as e:
            logger.error(f"Failed to send message to Kafka: {str(e)}")
    else:
        logger.error("Kafka producer is not initialized")

generator = GeoDataGenerator()
logger = logging.getLogger(__name__)

async def generate_and_send_data_continuously():
    while True:
        data = generator.get_json_data()
        send_to_kafka('geo_data', data)
        logger.info(f"Sent data to Kafka: {data}")
        await asyncio.sleep(0.1)  # Generate and send data every second