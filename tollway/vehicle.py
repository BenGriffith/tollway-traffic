from random import choice

from faker import Faker
from faker_vehicle import VehicleProvider
from us.states import STATES


def create_vehicle(fake: Faker) -> dict:
    
    vehicle = {f"{key.lower()}": value for key, value in fake.vehicle_object().items()}
    vehicle["license_plate"] = fake.license_plate()
    vehicle["vin"] = fake.vin()
    vehicle["state"] = choice(STATES).abbr
    vehicle["primary_color"] = fake.color_name()

    return vehicle


def create_tollway(tollways: list[str]) -> dict:
    pass
    # vehicle["tollway"]
    # vehicle[""]


def create_message() -> None:
    pass
    

if __name__ == "__main__":
    fake = Faker()
    fake.add_provider(VehicleProvider)
    vehicle = create_vehicle(fake=fake)