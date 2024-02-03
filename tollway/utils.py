import json
from pathlib import Path
from typing import Mapping, TypedDict, Union

from decouple import config
from google.cloud import pubsub_v1
from google.oauth2 import service_account


class EventsLog(TypedDict):
    late_events: dict[str, list[str]]
    past_events: list[dict[str, str]]
    all_events: list[Mapping[str, Union[str, bool]]]


def get_topic(pubsub: bool) -> tuple:
    if pubsub:
        project = config("PROJECT_ID")
        topic = config("TOPIC_ID")
        credentials = service_account.Credentials.from_service_account_file(config("PUBSUB_SERVICE_ACCOUNT"))
        publisher = pubsub_v1.PublisherClient(credentials=credentials)
        topic_path = publisher.topic_path(project=project, topic=topic)
        return publisher, topic_path
    return None, None


def encode_message(message: dict) -> bytes:
    return json.dumps(message).encode("utf-8")


def write_to_file(filename: str, events_log: list[Mapping[str, Union[str, bool]]]):
    path = Path().absolute()
    with open(path / filename, mode="a") as file:
        json.dump(obj=events_log, fp=file, indent=1)


def get_envs() -> dict:
    envs = {}

    duplicate_rate = config("DUPLICATE_RATE", default=50)
    all_events_count = config("ALL_EVENTS_COUNT", default=250)
    late_seconds_rate = config("LATE_SECONDS_RATE", default=10)
    late_minutes_rate = config("LATE_MINUTES_RATE", default=20)
    late_hours_rate = config("LATE_HOURS_RATE", default=30)
    late_days_rate = config("LATE_DAYS_RATE", default=100)

    if duplicate_rate == "":
        duplicate_rate = 50
    if all_events_count == "":
        all_events_count = 250
    if late_seconds_rate == "":
        late_seconds_rate = 10
    if late_minutes_rate == "":
        late_minutes_rate = 20
    if late_hours_rate == "":
        late_hours_rate = 30
    if late_days_rate == "":
        late_days_rate = 100

    envs["duplicate_rate"] = duplicate_rate
    envs["all_events_count"] = all_events_count
    envs["late_seconds_rate"] = late_seconds_rate
    envs["late_minutes_rate"] = late_minutes_rate
    envs["late_hours_rate"] = late_hours_rate
    envs["late_days_rate"] = late_days_rate

    return envs
