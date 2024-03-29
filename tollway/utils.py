import json
import logging
from pathlib import Path
from typing import Callable, Mapping, NamedTuple, Optional, TypedDict, Union

from decouple import config
from google.api_core.exceptions import GoogleAPICallError, RetryError
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.publisher.futures import Future
from google.oauth2 import service_account


class Topic(NamedTuple):
    publisher: pubsub_v1.PublisherClient
    topic_path: Optional[str] = None


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


def future_callback(logger: logging.Logger, event_message: dict[str, str]) -> Callable[[Future], None]:
    def callback(future: Future) -> None:
        try:
            message_id = future.result()
            event_message["pubsub_message_id"] = message_id
            logger.info(f"Message published with ID: {message_id}")
        except GoogleAPICallError as e:
            logger.error(f"A Google API call error occurred: {e}")
        except RetryError as e:
            logger.error(f"A retry error occurred: {e}")
        except Exception as e:
            logger.exception("An unexpected exception occurred")

    return callback


def write_to_file(filename: str, events_log: list[Mapping[str, Union[str, bool]]]):
    path = Path().absolute()
    with open(path / filename, mode="a") as file:
        json.dump(obj=events_log, fp=file, indent=1)


def get_config_with_default(key: str, default_value: int) -> int:
    value = config(key, default=default_value)
    return default_value if value == "" else int(value)
