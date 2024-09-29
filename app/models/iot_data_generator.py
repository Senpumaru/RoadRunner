# iot_data_generator.py

import random
import time
from dataclasses import dataclass, asdict
import json

@dataclass
class IoTData:
    device_id: str
    timestamp: float
    temperature: float
    humidity: float
    pressure: float
    battery_level: float

class IoTDataGenerator:
    def __init__(self, num_devices=1000, outlier_probability=0.05):
        self.num_devices = num_devices
        self.devices = [f"device_{i:04d}" for i in range(num_devices)]
        self.outlier_probability = outlier_probability

    def generate_data(self):
        device = random.choice(self.devices)
        is_outlier = random.random() < self.outlier_probability

        if is_outlier:
            temperature = random.uniform(-50, 150)  # Wider range for outliers
        else:
            temperature = random.uniform(-20, 50)  # Normal range

        return IoTData(
            device_id=device,
            timestamp=time.time(),
            temperature=temperature,
            humidity=random.uniform(0, 100),
            pressure=random.uniform(900, 1100),
            battery_level=random.uniform(0, 100)
        )

    def get_json_data(self):
        return json.dumps(asdict(self.generate_data()))