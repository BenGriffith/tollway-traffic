import unicodedata
from random import choice
from typing import Optional
from datetime import datetime, timezone

import requests
from faker import Faker
from bs4 import BeautifulSoup
from us.states import STATES_AND_TERRITORIES


STATE_NAMES = [state.name for state in STATES_AND_TERRITORIES]
TOLLWAYS_URL = "https://en.wikipedia.org/wiki/List_of_toll_roads_in_the_United_States"
TIMESTAMP_FORMAT = "%Y-%m-%d %M:%H:%S.%f %Z"


def create_vehicle(fake: Faker) -> dict:

    vehicle = {key.lower(): value for key, value in fake.vehicle_object().items()}
    vehicle["license_plate"] = fake.license_plate()
    vehicle["vin"] = fake.vin()
    vehicle["state"] = choice(STATES_AND_TERRITORIES).abbr
    vehicle["primary_color"] = fake.color_name()

    return vehicle


def get_tollways(html: Optional[str] = None) -> dict:
    if html is None:
        html = requests.get(TOLLWAYS_URL)

    page = BeautifulSoup(markup=html.text, features="html.parser")
    soup = page.find("div", class_="mw-parser-output")

    states = [h2.text.replace("[edit]", "") for h2 in soup.find_all("h2")]

    tables = []
    for h2 in soup.find_all("h2"):
        if h2.span.string not in STATE_NAMES:
            continue

        tolls = []
        for sibling in h2.find_next_siblings():
            if sibling.name == "table":
                tolls.extend(
                    [
                        unicodedata.normalize("NFKD", td.text.strip())
                        for tr in sibling.find_all("tr")
                        if (td := tr.find("td")) is not None
                    ]
                )
            # don't include tables after the next h2
            if sibling.name == "h2":
                break

        tables.append(tolls)

    united_states_tollways = dict(
        (state, tolls) for state, tolls in zip(states, tables) if tolls
    )
    return united_states_tollways


def create_tollway(tollways: dict) -> tuple[str, str]:
    state = choice(list(tollways.keys()))  
    name = choice(tollways[state])
    return state, name


def create_payload(vehicle: dict, tollway: tuple) -> dict:
    tollway = {
        "tollway_state": tollway[0],
        "tollway_name": tollway[1],
    }
    vehicle.update(tollway)
    vehicle["timestamp"] = datetime.now(tz=timezone.utc).strftime(TIMESTAMP_FORMAT)
    return vehicle