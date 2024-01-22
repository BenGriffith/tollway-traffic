import json
from pathlib import Path
from typing import Optional, TypedDict

from google.cloud import pubsub_v1
from google.pubsub_v1 import PubsubMessage

from tollway.constants import PROJECT_ID, TOPIC_ID


class TollwayMessage(TypedDict):
    year: str
    make: str
    model: str
    category: str
    license_plate: str
    vin: str
    state: str
    primary_color: str
    tollway_state: str
    tollway_name: str
    timestamp: str
    is_late: Optional[str]
    is_duplicate: Optional[bool]


class EventsLog(TypedDict):
    late_events: dict[str, list[str]]
    past_events: list[TollwayMessage]
    all_events: list[TollwayMessage]


def get_topic(pubsub: bool) -> tuple:
    if pubsub:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project=PROJECT_ID, topic=TOPIC_ID)
        return publisher, topic_path
    return None, None


def encode_message(message: TollwayMessage) -> PubsubMessage:
    return PubsubMessage(json.dumps(message).encode("utf-8"))


def write_to_file(filename: str, events_log: list[dict]):
    path = Path().absolute()
    with open(path / filename, mode="a") as file:
        json.dump(obj=events_log, fp=file, indent=1)
