import time

import typer
from faker import Faker
from faker_vehicle import VehicleProvider
from typing_extensions import Annotated

from tollway.callbacks import (
    event_rate_callback,
    filename_callback,
    total_event_callback,
)
from tollway.constants import ALL_EVENTS_COUNT, FILENAME, Help
from tollway.events import DuplicateEventProcessor, LateEventProcessor
from tollway.pubsub_logging import get_pubsub_logger
from tollway.utils import (
    EventsLog,
    encode_message,
    future_callback,
    get_topic,
    write_to_file,
)
from tollway.vehicle import create_message, create_tollway, create_vehicle, get_tollways

app = typer.Typer()
tollways = get_tollways()
fake = Faker()
fake.add_provider(VehicleProvider)


@app.command()
def main(
    total_events: Annotated[
        int, typer.Option(help=Help.TOTAL_EVENTS.value, callback=total_event_callback)
    ] = 1,
    event_rate: Annotated[
        float, typer.Option(help=Help.EVENT_RATE.value, callback=event_rate_callback)
    ] = 1.0,
    output_file: Annotated[bool, typer.Option(help=Help.OUTPUT_FILE.value)] = False,
    output_filename: Annotated[
        str, typer.Option(help=Help.OUTPUT_FILENAME.value, callback=filename_callback)
    ] = FILENAME,
    include_late_seconds: Annotated[bool, typer.Option(help=Help.INCLUDE_LATE_SECONDS.value)] = False,
    include_late_minutes: Annotated[bool, typer.Option(help=Help.INCLUDE_LATE_MINUTES.value)] = False,
    include_late_hours: Annotated[bool, typer.Option(help=Help.INCLUDE_LATE_HOURS.value)] = False,
    include_late_days: Annotated[bool, typer.Option(help=Help.INCLUDE_LATE_DAYS.value)] = False,
    include_duplicate: Annotated[bool, typer.Option(help=Help.INCLUDE_DUPLICATE.value)] = False,
    pubsub: Annotated[bool, typer.Option(help=Help.PUBSUB.value)] = False,
):

    events_log: EventsLog = {
        "late_events": {
            "seconds": [],
            "minutes": [],
            "hours": [],
            "days": [],
        },
        "past_events": [],
        "all_events": [],
    }

    # pubsub initial setup
    publisher, topic_path = get_topic(pubsub=pubsub)
    pubsub_logger = get_pubsub_logger(pubsub=pubsub)

    for event_count in range(total_events):

        # to control events_log["all_events"] logging
        late_processed = False
        duplicate_processed = False

        # create new event
        tollway = create_tollway(tollways=tollways)
        vehicle = create_vehicle(fake=fake)
        message = create_message(vehicle=vehicle, tollway=tollway)

        # LATE EVENTS
        if include_late_seconds:
            events_log["late_events"]["seconds"].append(message["timestamp"])

        if include_late_minutes:
            events_log["late_events"]["minutes"].append(message["timestamp"])

        if include_late_hours:
            events_log["late_events"]["hours"].append(message["timestamp"])

        if include_late_days:
            events_log["late_events"]["days"].append(message["timestamp"])

        if any([include_late_seconds, include_late_minutes, include_late_hours, include_late_days]):
            late_event = LateEventProcessor(
                events_log=events_log,
                publisher=publisher,
                topic_path=topic_path,
                fake=fake,
                tollways=tollways,
            )
            events_log, late_processed = late_event.process_event(pubsub_logger=pubsub_logger)

        # DUPLICATE EVENTS
        if include_duplicate:
            events_log["past_events"].append(message)
            duplicate_event = DuplicateEventProcessor(
                events_log=events_log,
                publisher=publisher,
                topic_path=topic_path,
            )
            events_log, duplicate_processed = duplicate_event.process_event(pubsub_logger=pubsub_logger)

        # captures all events except late and duplicate
        if pubsub:
            data = encode_message(message=message)
            future = publisher.publish(topic=topic_path, data=data)
            future.add_done_callback(future_callback(logger=pubsub_logger, event_message=message))

        if not late_processed and not duplicate_processed:
            events_log["all_events"].append(message)

        if len(events_log["all_events"]) == ALL_EVENTS_COUNT:
            if output_file:
                write_to_file(filename=output_filename, events_log=events_log["all_events"])
            events_log["all_events"] = []

        time.sleep(event_rate)

    # when iterating stops, if any events events remain in events_log["all_events"]
    # they will be handled here
    if output_file and len(events_log["all_events"]) > 0:
        write_to_file(filename=output_filename, events_log=events_log["all_events"])


if __name__ == "__main__":
    app()
