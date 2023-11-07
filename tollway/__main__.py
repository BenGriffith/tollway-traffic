from faker import Faker
from faker_vehicle import VehicleProvider

from vehicle import get_tollways, create_tollway, create_vehicle, create_message

tollways = get_tollways()
fake = Faker()
fake.add_provider(VehicleProvider)


if __name__ == "__main__":
    tollway = create_tollway(tollways)
    vehicle = create_vehicle(fake=fake)
    payload = create_message(vehicle=vehicle, tollway=tollway)