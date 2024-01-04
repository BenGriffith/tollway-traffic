import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import TypedDict

from decouple import config
from google.cloud import pubsub_v1
from google.pubsub_v1 import PubsubMessage

from tollway.constants import DATE_VARIATION_MAX, DATE_VARIATION_MIN, TIMESTAMP_FORMAT


class EventsLog(TypedDict):
    past_events_timestamps: list[str]
    past_events: list[dict[str, str]]
    all_events: list[dict[str, str]]


def get_date_variation(timestamp: str) -> str:
    random_integer = random.randint(DATE_VARIATION_MIN, DATE_VARIATION_MAX)
    current_timestamp = datetime.strptime(timestamp, TIMESTAMP_FORMAT)
    updated_timestamp = (current_timestamp - timedelta(days=random_integer)).strftime(TIMESTAMP_FORMAT)
    return updated_timestamp


def get_topic(pubsub: bool) -> tuple:
    if pubsub:
        project_id = config("PROJECT_ID")
        topic_id = config("TOPIC_ID")
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project=project_id, topic=topic_id)
        return publisher, topic_path
    return None, None


def encode_message(payload: dict) -> PubsubMessage:
    return PubsubMessage(json.dumps(payload).encode("utf-8"))


def write_to_file(filename: str, events_log: list[dict]):
    path = Path().absolute()
    with open(path / filename, mode="a") as file:
        json.dump(obj=events_log, fp=file, indent=4)
