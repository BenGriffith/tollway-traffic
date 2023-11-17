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