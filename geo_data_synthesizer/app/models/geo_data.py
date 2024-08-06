import random
import time
from dataclasses import dataclass, asdict
import json

@dataclass
class GeoData:
    device_id: str
    timestamp: float
    latitude: float
    longitude: float
    speed: float
    direction: float

class GeoDataGenerator:
    def __init__(self, num_devices=10):
        self.num_devices = num_devices
        self.devices = [f"device_{i}" for i in range(num_devices)]

    def generate_data(self):
        device = random.choice(self.devices)
        return GeoData(
            device_id=device,
            timestamp=time.time(),
            latitude=random.uniform(-90, 90),
            longitude=random.uniform(-180, 180),
            speed=random.uniform(0, 120),
            direction=random.uniform(0, 360)
        )

    def get_json_data(self):
        return json.dumps(asdict(self.generate_data()))