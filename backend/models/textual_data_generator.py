# textual_data_generator.py

import random
import time
from dataclasses import dataclass, asdict
import json

@dataclass
class TextualData:
    device_id: str
    timestamp: float
    status_message: str
    log_entry: str

class TextualDataGenerator:
    def __init__(self, num_devices=1000):
        self.num_devices = num_devices
        self.devices = [f"device_{i:04d}" for i in range(num_devices)]
        self.status_messages = [
            "Operating normally",
            "Low battery warning",
            "Maintenance required",
            "Firmware update available",
            "Sensor malfunction detected"
        ]
        self.log_entry_templates = [
            "Device {device_id} reported {status} at {timestamp}",
            "Alert: {status} for device {device_id}",
            "Maintenance log: {status}",
            "System message: {status}"
        ]

    def generate_data(self):
        device = random.choice(self.devices)
        status = random.choice(self.status_messages)
        timestamp = time.time()
        log_entry = random.choice(self.log_entry_templates).format(
            device_id=device,
            status=status,
            timestamp=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        )
        return TextualData(
            device_id=device,
            timestamp=timestamp,
            status_message=status,
            log_entry=log_entry
        )

    def get_json_data(self):
        return json.dumps(asdict(self.generate_data()))