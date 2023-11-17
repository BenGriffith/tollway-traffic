import time
import random
from typing import Optional

import typer
from faker import Faker
from faker_vehicle import VehicleProvider

from tollway.vehicle import get_tollways, create_tollway, create_vehicle, create_payload
from tollway.utils import get_date_variation, get_random_timestamp, write_to_file
from tollway.constants import DATE_VARIATION_RATE, INCLUDE_LATE_RATE, INCLUDE_DUPLICATE_RATE, ALL_EVENTS_COUNT


tollways = get_tollways()
fake = Faker()
fake.add_provider(VehicleProvider)


def main(
        total_events: Optional[int] = typer.Option(default=1),
        event_rate: Optional[float] = typer.Option(default=1.0),
        output_file: Optional[bool] = typer.Option(default=False),
        output_filename: Optional[str] = typer.Option(default="tollway-traffic.json"),
        date_variation: Optional[bool] = typer.Option(default=False),
        include_late: Optional[bool] = typer.Option(default=False),
        include_duplicate: Optional[bool] = typer.Option(default=False),
        ):

    tollway = create_tollway(tollways)
    date_variation_events = []
    past_events_timestamps = []
    past_events = []
    all_events = []

    for event_count in range(total_events):
        vehicle = create_vehicle(fake=fake)
        payload = create_payload(vehicle=vehicle, tollway=tollway)

        if date_variation:
            if event_count % DATE_VARIATION_RATE == 0:
                payload["timestamp"] = get_date_variation(timestamp=payload.get("timestamp"))
            date_variation_events.append(payload)
            continue

        if include_late:
            past_events_timestamps.append(payload.get("timestamp"))
        
        if include_duplicate:
            past_events.append(payload)

        if len(past_events_timestamps) == INCLUDE_LATE_RATE:
            late_vehicle = create_vehicle(fake=fake)
            late_event = create_payload(vehicle=late_vehicle, tollway=tollway)

            random_timestamp = get_random_timestamp(timestamps=past_events_timestamps)
            late_event["timestamp"] = random_timestamp

            # push late event to topic
            all_events.append(late_event)
            past_events = []
            continue

        if len(past_events) == INCLUDE_DUPLICATE_RATE:
            duplicate_event = random.choice(past_events)

            # push duplicate event to topic
            all_events.append(duplicate_event)
            past_events = []
            continue

        # push event to topic

        all_events.append(payload)

        if output_file and len(all_events) == ALL_EVENTS_COUNT:
            write_to_file(filename=output_filename, events=all_events)
        time.sleep(event_rate)

    if date_variation:
        write_to_file(filename=output_file, events=date_variation_events)
        # push to topic
    
    
if __name__ == "__main__":
    typer.run(main)