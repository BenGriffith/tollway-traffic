import random

from faker import Faker

from tollway.vehicle import create_payload, create_vehicle


def create_late_event(events_log: dict, fake: Faker, tollway: dict) -> dict:
    past_timestamps = events_log.get("past_events_timestamps")
    late_event_vehicle = create_vehicle(fake)
    late_event_payload = create_payload(late_event_vehicle, tollway)
    random_ts = random.choice(past_timestamps[slice(0, len(past_timestamps))])
    late_event_payload["timestamp"] = random_ts
    return late_event_payload


def process_late_event(events_log: dict, fake: Faker, tollway: dict) -> dict:
    late_event_payload = create_late_event(events_log, fake, tollway)

    # push to topic
    events_log.get("all_events").append(late_event_payload)
    events_log["past_events_timestamps"] = []
    return events_log


def create_duplicate_event(events_log: dict) -> dict:
    duplicate_event = random.choice(events_log.get("past_events"))
    return duplicate_event


def process_duplicate_event(events_log: dict) -> dict:
    duplicate_event = create_duplicate_event(events_log)

    # push to topic
    events_log.get("all_events").append(duplicate_event)
    events_log["past_events"] = []
    return events_log
