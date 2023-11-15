from enum import Enum

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
def vehicle_constants():
    vehicle_constants = {
        "STATES": 29,
        "ALABAMA": 4,
        "CALIFORNIA": 16,
        "COLORADO": 8,
        "DELAWARE": 3,
        "FLORIDA": 35,
        "GEORGIA": 4,
        "ILLINOIS": 6,
        "INDIANA": 1,
        "KANSAS": 1,
        "LOUISIANA": 1,
        "MAINE": 1,
        "MARYLAND": 3,
        "MASSACHUSETTS": 1,
        "MINNESOTA": 4,
        "NEW HAMPSHIRE": 3,
        "NEW JERSEY": 5,
        "NEW YORK": 3,
        "NORTH CAROLINA": 3,
        "OHIO": 1,
        "OKLAHOMA": 11,
        "PENNSYLVANIA": 6,
        "PUERTO RICO": 8,
        "RHODE ISLAND": 5,
        "SOUTH CAROLINA": 1,
        "TEXAS": 38,
        "UTAH": 2,
        "VIRGINIA": 12,
        "WASHINGTON": 2,
        "WEST VIRGINIA": 1,
        "PAYLOAD_LENGTH": 11 
    }

    return vehicle_constants


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