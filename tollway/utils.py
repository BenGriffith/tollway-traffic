import random
import json
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum

from tollway.constants import TIMESTAMP_FORMAT


def get_random_timestamp(timestamps: list[str]) -> str:
    first_timestamp = datetime.strptime(timestamps[0], TIMESTAMP_FORMAT)
    middle_timestamp = datetime.strptime(timestamps[len(timestamps) // 2], TIMESTAMP_FORMAT)

    random_percentage = random.random()
    timestamp_range = middle_timestamp - first_timestamp
    random_timestamp = (first_timestamp + random_percentage * timestamp_range).strftime(TIMESTAMP_FORMAT)
    return random_timestamp


def push_to_topic():
    pass # to be developed


def write_to_file(filename: str, events: list[dict]):
    path = str(Path().absolute())
    with open(f"{path}/{filename}", mode="a") as file:
        json.dump(obj=events, fp=file, indent=4)


def get_date_variation(timestamp: str) -> str:
    random_integer = random.randint(1, 3)
    current_timestamp = datetime.strptime(timestamp, TIMESTAMP_FORMAT)
    updated_timestamp = (current_timestamp - timedelta(days=random_integer)).strftime(TIMESTAMP_FORMAT)
    return updated_timestamp


