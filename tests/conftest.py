import pytest
from faker import Faker
from faker_vehicle import VehicleProvider

from tollway.vehicle import create_vehicle, STATES_AND_TERRITORIES


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