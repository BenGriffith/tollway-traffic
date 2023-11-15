import random
import json
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum

from us.states import STATES_AND_TERRITORIES


class Constants(Enum):
    STATE_NAMES = [state.name for state in STATES_AND_TERRITORIES]
    TOLLWAYS_URL = "https://en.wikipedia.org/wiki/List_of_toll_roads_in_the_United_States"
    TIMESTAMP_FORMAT = "%Y-%m-%d %M:%H:%S.%f %Z"
    DATE_VARIATION_RATE = 3
    INCLUDE_LATE_RATE = 20
    INCLUDE_DUPLICATE_RATE = 50
    ALL_EVENTS_COUNT = 100


def get_random_timestamp(timestamps: list[str]) -> str:
    first_timestamp = datetime.strptime(timestamps[0], Constants.TIMESTAMP_FORMAT.value)
    middle_timestamp = datetime.strptime(timestamps[len(timestamps) // 2], Constants.TIMESTAMP_FORMAT.value)

    random_percentage = random.random()
    timestamp_range = middle_timestamp - first_timestamp
    random_timestamp = (first_timestamp + random_percentage * timestamp_range).strftime(Constants.TIMESTAMP_FORMAT.value)
    return random_timestamp


def push_to_topic():
    pass # to be developed


def write_to_file(filename: str, events: list[dict]):
    path = str(Path().absolute())
    with open(f"{path}/{filename}", mode="a") as file:
        json.dump(obj=events, fp=file, indent=4)


def get_date_variation(timestamp: str) -> str:
    random_integer = random.randint(1, 3)
    current_timestamp = datetime.strptime(timestamp, Constants.TIMESTAMP_FORMAT.value)
    updated_timestamp = (current_timestamp - timedelta(days=random_integer)).strftime(Constants.TIMESTAMP_FORMAT.value)
    return updated_timestamp


