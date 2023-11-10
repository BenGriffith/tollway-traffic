import time
from typing import Optional

import typer
from faker import Faker
from faker_vehicle import VehicleProvider

from tollway.vehicle import get_tollways, create_tollway, create_vehicle, create_message

tollways = get_tollways()
fake = Faker()
fake.add_provider(VehicleProvider)


def main(
        total_events: Optional[int] = typer.Option(default=1),
        streaming_rate: Optional[int] = typer.Option(default=1),
        output_file: Optional[bool] = typer.Option(default=False),
        date_variation: Optional[bool] = typer.Option(default=False),
        include_late: Optional[bool] = typer.Option(default=False)
        ):

    tollway = create_tollway(tollways)

    for message_count in range(total_events):
        vehicle = create_vehicle(fake=fake) # update date use in create_vehicle
        payload = create_message(vehicle=vehicle, tollway=tollway)

        time.sleep(streaming_rate)
    

if __name__ == "__main__":
    typer.run(main)