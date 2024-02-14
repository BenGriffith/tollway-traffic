import time
from datetime import datetime

import pytest
from faker import Faker
from faker_vehicle import VehicleProvider

from tollway.constants import TIME_UNIT, TIMESTAMP_FORMAT
from tollway.events import DuplicateEventProcessor, LateEventProcessor
from tollway.utils import get_topic
from tollway.vehicle import (
    STATES_AND_TERRITORIES,
    create_message,
    create_tollway,
    create_vehicle,
    get_tollways,
)


@pytest.fixture
def faker_vehicle():
    fake = Faker()
    fake.add_provider(VehicleProvider)
    return {"faker": fake, "states": STATES_AND_TERRITORIES}


@pytest.fixture
def vehicle(faker_vehicle):
    return create_vehicle(fake=faker_vehicle.get("faker"))


@pytest.fixture(scope="session")
def tollways():
    return get_tollways()


@pytest.fixture
def get_tollway(tollways):
    return create_tollway(tollways=tollways)


@pytest.fixture
def message(vehicle, get_tollway):
    return create_message(vehicle=vehicle, tollway=get_tollway)


@pytest.fixture
def messages(faker_vehicle, get_tollway):
    _messages = []
    for _ in range(30):
        vehicle = create_vehicle(fake=faker_vehicle.get("faker"))
        message = create_message(vehicle=vehicle, tollway=get_tollway)
        _messages.append(message)
        time.sleep(0.1)
    return _messages


@pytest.fixture
def events_log_init():
    events_log = {
        "late_events": {
            "seconds": [],
            "minutes": [],
            "hours": [],
            "days": [],
        },
        "past_events": [],
        "all_events": [],
    }
    return events_log


@pytest.fixture
def events_log(messages, events_log_init):
    late_events_messages = [message.get("timestamp") for message in messages]
    events_log_init["late_events"]["seconds"] = late_events_messages
    events_log_init["late_events"]["minutes"] = late_events_messages
    events_log_init["late_events"]["hours"] = late_events_messages
    events_log_init["late_events"]["days"] = late_events_messages
    return events_log_init


@pytest.fixture
def past_events(messages, events_log_init):
    events_log_init["past_events"] = messages
    return events_log_init


@pytest.fixture
def pubsub():
    return get_topic(pubsub=False)


@pytest.fixture
def late_events(faker_vehicle, events_log, pubsub, tollways):
    late_event = LateEventProcessor(
        events_log=events_log,
        publisher=pubsub.publisher,
        topic_path=pubsub.topic_path,
        fake=faker_vehicle["faker"],
        tollways=tollways,
    )
    late_events = {}
    for time_unit in TIME_UNIT.keys():
        late_event.time_unit = time_unit
        late_events[time_unit] = late_event.create_event()
    return late_events


@pytest.fixture
def generate_event_pair(late_events, events_log):
    def _generate_event_pair(time_unit):
        late_event_timestamp = late_events[time_unit]["timestamp"]
        late_event_microseconds = datetime.strptime(late_event_timestamp, TIMESTAMP_FORMAT).microsecond

        for original_event_timestamp in events_log["late_events"][time_unit]:
            original_event_microseconds = datetime.strptime(
                original_event_timestamp, TIMESTAMP_FORMAT
            ).microsecond
            # Compare the microseconds part of the timestamps
            if late_event_microseconds == original_event_microseconds:
                return {
                    "original": datetime.strptime(original_event_timestamp, TIMESTAMP_FORMAT),
                    "late": datetime.strptime(late_event_timestamp, TIMESTAMP_FORMAT),
                }
        return {}

    return _generate_event_pair


@pytest.fixture
def original_and_late_events_timestamps(generate_event_pair):
    event_pairs = {}
    for time_unit in TIME_UNIT.keys():
        event_pair = generate_event_pair(time_unit)
        if event_pair:
            event_pairs[time_unit] = event_pair
    return event_pairs


@pytest.fixture
def duplicate_event(past_events, pubsub):
    event = DuplicateEventProcessor(
        events_log=past_events,
        publisher=pubsub.publisher,
        topic_path=pubsub.topic_path,
    )
    duplicate = event.create_event()
    return duplicate
