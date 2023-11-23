import json
import random
from datetime import datetime, timedelta
from pathlib import Path

from google.cloud import pubsub_v1

from tollway.constants import PROJECT_ID, TIMESTAMP_FORMAT, TOPIC_ID


def get_date_variation(timestamp: str) -> str:
    random_integer = random.randint(1, 3)
    current_timestamp = datetime.strptime(timestamp, TIMESTAMP_FORMAT)
    updated_timestamp = (current_timestamp - timedelta(days=random_integer)).strftime(TIMESTAMP_FORMAT)
    return updated_timestamp


def get_topic():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project=PROJECT_ID, topic=TOPIC_ID)
    return publisher, topic_path


def encode_message(payload: dict) -> json:
    return json.dumps(payload).encode("utf-8")


def write_to_file(filename: str, events_log: list[dict]):
    path = Path().absolute()
    with open(path / filename, mode="a") as file:
        json.dump(obj=events_log, fp=file, indent=4)
