import random
from datetime import datetime, timedelta

from faker import Faker
from google.pubsub_v1 import PublisherClient, Topic

from tollway.utils import EventsLog, encode_message
from tollway.vehicle import create_message, create_tollway, create_vehicle
from tollway.constants import TIME_UNIT, TIMESTAMP_FORMAT


def _calculate_late_timestamp(time_unit: str, ts: str) -> str:
    random_integer = random.randint(TIME_UNIT[time_unit]["min"], TIME_UNIT[time_unit]["max"])
    current_timestamp = datetime.strptime(ts, TIMESTAMP_FORMAT)
    return (current_timestamp - timedelta(**{time_unit: random_integer})).strftime(TIMESTAMP_FORMAT)


def create_late_event(events_log: EventsLog, fake: Faker, tollways: dict, time_unit: str) -> dict:
    past_timestamps = events_log["late_events"][time_unit]
    late_event_tollway = create_tollway(tollways=tollways)
    late_event_vehicle = create_vehicle(fake)
    late_event_message = create_message(late_event_vehicle, late_event_tollway)
    random_ts = random.choice(past_timestamps[slice(0, len(past_timestamps))])
    late_event_message["timestamp"] = _calculate_late_timestamp(time_unit=time_unit, ts=random_ts)
    return late_event_message


def process_late_event(
    events_log: EventsLog,
    fake: Faker,
    tollways: dict,
    publisher: PublisherClient,
    topic_path: Topic,
    time_unit: str,
) -> EventsLog:
    late_event_message = create_late_event(events_log, fake, tollways, time_unit)
    if publisher and topic_path:
        data = encode_message(message=late_event_message)
        future = publisher.publish(topic=topic_path, messages=data)
    events_log["all_events"].append(late_event_message)
    events_log["late_events"][time_unit] = []
    return events_log


def create_duplicate_event(events_log: EventsLog) -> dict[str, str]:
    duplicate_event = random.choice(events_log["past_events"])
    return duplicate_event


def process_duplicate_event(events_log: EventsLog, publisher: PublisherClient, topic_path: Topic) -> EventsLog:
    duplicate_event = create_duplicate_event(events_log)
    if publisher and topic_path:
        data = encode_message(message=duplicate_event)
        future = publisher.publish(topic=topic_path, messages=data)
    events_log["all_events"].append(duplicate_event)
    events_log["past_events"] = []
    return events_log
