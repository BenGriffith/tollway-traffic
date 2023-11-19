import time
import random
from typing import Optional

import typer
from faker import Faker
from faker_vehicle import VehicleProvider

from tollway.vehicle import get_tollways, create_tollway, create_vehicle, create_payload
from tollway.utils import get_date_variation, write_to_file
from tollway.constants import DATE_VARIATION_RATE, INCLUDE_LATE_RATE, INCLUDE_DUPLICATE_RATE, ALL_EVENTS_COUNT
from tollway.events import process_late_event, process_duplicate_event


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
    events_log = {
        "past_events_timestamps": [],
        "past_events": [],
        "all_events": [],
    }

    if date_variation:
        include_late = False
        include_duplicate = False

    for event_count in range(total_events):

        # create new event
        vehicle = create_vehicle(fake=fake)
        payload = create_payload(vehicle=vehicle, tollway=tollway)

        # DATE VARIATION
        if date_variation and event_count % DATE_VARIATION_RATE == 0:
            payload["timestamp"] = get_date_variation(timestamp=payload.get("timestamp"))
            # push to topic
            continue

        # LATE EVENTS
        if include_late:
            if len(events_log.get("past_events_timestamps")) == INCLUDE_LATE_RATE:
                events_log = process_late_event(events_log=events_log, fake=fake, tollway=tollway)
            events_log.get("past_events_timestamps").append(payload.get("timestamp"))
            continue

        # DUPLICATE EVENTS        
        if include_duplicate:
            if len(events_log.get("past_events")) == INCLUDE_DUPLICATE_RATE:
                events_log = process_duplicate_event(events_log=events_log)
            events_log.get("past_events").append(payload)
            continue

        # captures all events except late and duplicate
        events_log.get("all_events").append(payload)

        if output_file and len(events_log.get("all_events")) == ALL_EVENTS_COUNT:
            write_to_file(filename=output_filename, events_log=events_log.get("all_events"))
            events_log["all_events"] = []
            
        time.sleep(event_rate)
    
    # when iterating stops, if any events events remain in events_log["all_events"] they will be handled here
    if output_file and len(events_log.get("all_events")) > 0:
        write_to_file(filename=output_filename, events_log=events_log.get("all_events"))
    
if __name__ == "__main__":
    typer.run(main)