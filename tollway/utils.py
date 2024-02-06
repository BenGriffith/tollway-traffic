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


def get_envs(env: str) -> int:
    defaults = {"duplicate": 50, "all": 250, "seconds": 10, "minutes": 20, "hours": 30, "days": 100}

    env_variable = config(env.upper(), default=defaults[env])
    if env_variable == "":
        return defaults[env]
    return env_variable
