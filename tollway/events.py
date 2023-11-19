import random

from faker import Faker

from tollway.vehicle import create_vehicle, create_payload


def create_late_event(events_log: dict, fake: Faker, tollway: dict) -> dict:
    late_event_vehicle = create_vehicle(fake=fake)
    late_event_payload = create_payload(vehicle=late_event_vehicle, tollway=tollway)

    late_event_payload["timestamp"] = random.choice(events_log.get("past_events_timestamps")[:len(events_log.get("past_events_timestamps"))])

    return late_event_payload


def process_late_event(events_log: dict, fake: Faker, tollway: dict) -> dict:
    late_event_payload = create_late_event(events_log=events_log, fake=fake, tollway=tollway)
    
    # push to topic
    events_log.get("all_events").append(late_event_payload)
    events_log["past_events_timestamps"] = []
    return events_log


def process_duplicate_event(events_log: dict) -> dict:
    duplicate_event = random.choice(events_log.get("past_events"))
    
    # push to topic
    events_log.get("all_events").append(duplicate_event)
    events_log["past_events"] = []
    return events_log