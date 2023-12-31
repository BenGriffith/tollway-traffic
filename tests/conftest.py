import time

import pytest
from faker import Faker
from faker_vehicle import VehicleProvider

from tollway.vehicle import (
    STATES_AND_TERRITORIES,
    create_message,
    create_tollway,
    create_vehicle,
    get_tollways,
)


@pytest.fixture
def setup():
    fake = Faker()
    fake.add_provider(VehicleProvider)
    return {"faker": fake, "states": STATES_AND_TERRITORIES}


@pytest.fixture
def vehicle(setup):
    return create_vehicle(fake=setup.get("faker"))


@pytest.fixture(scope="session")
def tollways():
    return get_tollways()


@pytest.fixture
def get_tollway(tollways):
    return create_tollway(tollways=tollways)


@pytest.fixture
def message(vehicle, get_tollway):
    return create_message(vehicle=vehicle, tollway=get_tollway)


@pytest.fixture()
def messages(setup, get_tollway):
    _messages = []
    for _ in range(30):
        vehicle = create_vehicle(fake=setup.get("faker"))
        message = create_message(vehicle=vehicle, tollway=get_tollway)
        _messages.append(message)
        time.sleep(0.1)
    return _messages


@pytest.fixture
def past_events_timestamps(messages):
    events_log = {"past_events_timestamps": [message.get("timestamp") for message in messages]}
    return events_log


@pytest.fixture
def past_events(messages):
    events_log = {"past_events": messages}
    return events_log
