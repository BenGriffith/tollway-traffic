from random import choice
from collections import defaultdict

import requests
from bs4 import BeautifulSoup, Tag
from faker import Faker
from faker_vehicle import VehicleProvider
from us.states import STATES_AND_TERRITORIES


STATE_NAMES = [state.name for state in STATES_AND_TERRITORIES]
TOLLWAYS_URL = "https://en.wikipedia.org/wiki/List_of_toll_roads_in_the_United_States"


def create_vehicle(fake: Faker) -> dict:

    vehicle = {f"{key.lower()}": value for key, value in fake.vehicle_object().items()}
    vehicle["license_plate"] = fake.license_plate()
    vehicle["vin"] = fake.vin()
    vehicle["state"] = choice(STATES_AND_TERRITORIES).abbr
    vehicle["primary_color"] = fake.color_name()

    return vehicle


def get_tollways(html: str | None = None) -> dict:
    if html is None:
        html = requests.get(TOLLWAYS_URL)

    page = BeautifulSoup(markup=html.text, features="html.parser")
    soup = page.find("div", class_="mw-parser-output")

    states = [h2.text.replace("[edit]", "") for h2 in soup.find_all('h2')]

    tables = []
    for h2 in soup.find_all('h2'):
        tolls = []

        for sibling in h2.find_next_siblings():
            if sibling.name == 'table':
                tolls.extend(
                    [td.text.strip() for tr in sibling.find_all('tr')
                    if (td := tr.find('td')) is not None]
                )
            # don't include tables after the next h2
            if sibling.name == 'h2':
                break

        tables.append(tolls)

    united_states_tollways = dict(
        (state, tolls) for state, tolls in zip(states, tables) if tolls
    )
    return united_states_tollways


def create_tollway(tollways: dict) -> [str, str]:
    state = choice([key for key in tollways.keys()])
    name = choice(list(tollways[state]))
    return state, name


def create_message() -> None:
    pass # placeholder - needs to be developed


# code below/like it will be moved to dunder main once module is complete
if __name__ == "__main__":
    tollways = get_tollways()
    tollway_state, tollway_name = create_tollway(tollways)
    breakpoint()
    fake = Faker()
    fake.add_provider(VehicleProvider)
    vehicle = create_vehicle(fake=fake)
