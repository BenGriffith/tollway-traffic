import time
import random
from typing import Optional
from datetime import datetime

import typer
from faker import Faker
from faker_vehicle import VehicleProvider

from tollway.vehicle import (
    get_tollways, 
    create_tollway, 
    create_vehicle, 
    create_message,
    TIMESTAMP_FORMAT,
)


DATE_VARIATION_RATE = random.randint(1, 3)
INCLUDE_LATE_RATE = 20
INCLUDE_DUPLICATE_RATE = 50

tollways = get_tollways()
fake = Faker()
fake.add_provider(VehicleProvider)


def _get_late_event(timestamps: list[str]) -> str:
    first_timestamp = datetime.strptime(timestamps[0], TIMESTAMP_FORMAT)
    middle_timestamp = datetime.strptime(timestamps[len(timestamps) // 2], TIMESTAMP_FORMAT)

    random_percentage = random.random()
    timestamp_range = middle_timestamp - first_timestamp
    random_timestamp = (first_timestamp + random_percentage * timestamp_range).strftime(TIMESTAMP_FORMAT)
    return random_timestamp


def _push_to_topic():
    pass # to be developed


def _write_to_file():
    pass # to be developed


def _date_variation():
    pass 


def main(
        total_events: Optional[int] = typer.Option(default=1),
        event_rate: Optional[int] = typer.Option(default=1),
        output_file: Optional[bool] = typer.Option(default=False),
        date_variation: Optional[bool] = typer.Option(default=False),
        date_variation_rate: Optional[int] = typer.Option(default=3),
        include_late: Optional[bool] = typer.Option(default=False),
        include_duplicate: Optional[bool] = typer.Option(default=False),
        ):

    tollway = create_tollway(tollways)
    date_variation_events = []
    past_events_timestamps = []
    past_events = []

    for _ in range(total_events):
        vehicle = create_vehicle(fake=fake)
        payload = create_message(vehicle=vehicle, tollway=tollway)

        if date_variation:
            date_variation_events.append(payload)
            continue

        if include_late:
            past_events_timestamps.append(payload.get("timestamp"))
        
        if include_duplicate:
            past_events.append(payload)

        if len(past_events_timestamps) == INCLUDE_LATE_RATE:
            late_vehicle = create_vehicle(fake=fake)
            late_payload = create_message(vehicle=late_vehicle, tollway=tollway)

            late_event = _get_late_event(timestamps=past_events_timestamps)
            late_payload["timestamp"] = late_event
            past_events = []

            # push late event to topic

            print("LATE EVENT", late_payload)

        if len(past_events) == INCLUDE_DUPLICATE_RATE:
            duplicate_event = random.choice(past_events)
            past_events = []

            # push duplicate event to topic

        time.sleep(event_rate)

    # for event in date_variation_events:

    

if __name__ == "__main__":
    typer.run(main)