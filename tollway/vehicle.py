from faker import Faker
from faker_vehicle import VehicleProvider


def create_vehicle(fake: Faker) -> dict:

    vehicle = {f"{key.lower()}": value for key, value in fake.vehicle_object().items()}
    vehicle["license plate"] = fake.license_plate()
    vehicle["vin"] = fake.vin()
    # vehicle["state"] = 

    return vehicle
    

if __name__ == "__main__":
    fake = Faker()
    fake.add_provider(VehicleProvider)
    vehicle = create_vehicle(fake=fake)
    breakpoint()