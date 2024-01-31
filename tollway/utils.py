import json
from pathlib import Path
from typing import Mapping, TypedDict, Union

from decouple import config
from google.cloud import pubsub_v1
from google.pubsub_v1 import PubsubMessage


class EventsLog(TypedDict):
    late_events: dict[str, list[str]]
    past_events: list[dict[str, str]]
    all_events: list[Mapping[str, Union[str, bool]]]


def get_topic(pubsub: bool) -> tuple:
    if pubsub:
        project = config("PROJECT_ID")
        topic = config("TOPIC_ID")
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project=project, topic=topic)
        return publisher, topic_path
    return None, None


def encode_message(message: dict) -> PubsubMessage:
    return PubsubMessage(json.dumps(message).encode("utf-8"))


def write_to_file(filename: str, events_log: list[Mapping[str, Union[str, bool]]]):
    path = Path().absolute()
    with open(path / filename, mode="a") as file:
        json.dump(obj=events_log, fp=file, indent=1)
