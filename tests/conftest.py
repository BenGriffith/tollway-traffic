import time

import pytest
from faker import Faker
from faker_vehicle import VehicleProvider

from tollway.vehicle import (
    create_vehicle, 
    get_tollways,
    create_tollway,
    create_payload,
    STATES_AND_TERRITORIES,
)


@pytest.fixture
def setup():
    fake = Faker()
    fake.add_provider(VehicleProvider)
    return {
        "faker": fake,
        "states": STATES_AND_TERRITORIES
    }


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
def payload(vehicle, get_tollway):
    return create_payload(vehicle=vehicle, tollway=get_tollway)


@pytest.fixture()
def payloads(setup, get_tollway):
    _payloads = []
    for _ in range(30):
        vehicle = create_vehicle(fake=setup.get("faker"))
        payload = create_payload(vehicle=vehicle, tollway=get_tollway)
        _payloads.append(payload)
        time.sleep(0.1)
    return _payloads


@pytest.fixture
def past_events_timestamps(payloads):
    events_log = {
        "past_events_timestamps": [payload.get("timestamp") for payload in payloads]
    }
    return events_log


@pytest.fixture
def past_events(payloads):
    events_log = {
        "past_events": payloads
    }
    return events_log