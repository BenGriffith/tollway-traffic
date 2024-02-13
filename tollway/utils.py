import json
import logging
from collections import namedtuple
from pathlib import Path
from typing import Mapping, TypedDict, Union

from decouple import config
from google.cloud import pubsub_v1
from google.oauth2 import service_account

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="pubsub.log",
    filemode="a",
)
logger = logging.getLogger("pubsub")

Topic = namedtuple("Topic", ["publisher", "topic_path"])


class EventsLog(TypedDict):
    late_events: dict[str, list[str]]
    past_events: list[dict[str, str]]
    all_events: list[Mapping[str, Union[str, bool]]]


def get_topic(pubsub: bool) -> Topic:
    if pubsub:
        project = config("PROJECT_ID")
        topic = config("TOPIC_ID")
        credentials = service_account.Credentials.from_service_account_file(config("PUBSUB_SERVICE_ACCOUNT"))
        publisher = pubsub_v1.PublisherClient(credentials=credentials)
        topic_path = publisher.topic_path(project=project, topic=topic)
        return Topic(publisher=publisher, topic_path=topic_path)
    return Topic(publisher=None, topic_path=None)


def encode_message(message: dict) -> bytes:
    return json.dumps(message).encode("utf-8")


def future_callback(future) -> None:
    try:
        message_id = future.result()
        logger.info(f"Message published with ID: {message_id}")
    except Exception as e:
        logger.error(f"An exception occurred: {e}")


def write_to_file(filename: str, events_log: list[Mapping[str, Union[str, bool]]]):
    path = Path().absolute()
    with open(path / filename, mode="a") as file:
        json.dump(obj=events_log, fp=file, indent=1)


def get_config_with_default(key: str, default_value: int) -> int:
    value = config(key, default=default_value)
    return default_value if value.strip() == "" else int(value)
