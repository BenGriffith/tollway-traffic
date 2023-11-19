import random
import json
from datetime import datetime, timedelta
from pathlib import Path

from tollway.constants import TIMESTAMP_FORMAT


def get_date_variation(timestamp: str) -> str:
    random_integer = random.randint(1, 3)
    current_timestamp = datetime.strptime(timestamp, TIMESTAMP_FORMAT)
    updated_timestamp = (current_timestamp - timedelta(days=random_integer)).strftime(TIMESTAMP_FORMAT)
    return updated_timestamp


def push_to_topic():
    pass # to be developed


def write_to_file(filename: str, events_log: list[dict]):
    path = Path().absolute()
    with open(path / filename, mode="a") as file:
        json.dump(obj=events_log, fp=file, indent=4)