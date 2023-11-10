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
        total_messages: Optional[int] = typer.Option(default=1),
        message_delay: Optional[int] = typer.Option(default=1)):

    tollway = create_tollway(tollways)

    for message_count in range(total_messages):
        vehicle = create_vehicle(fake=fake) # update date use in create_vehicle
        payload = create_message(vehicle=vehicle, tollway=tollway)

        time.sleep(message_delay)
    

    # number of messages - total_messages
    # time between messages - message_delay
    # number of messages in one day - create_in_day
        # different dates
    # late arriving events -> late_arriving or out_of_order



if __name__ == "__main__":
    typer.run(main)