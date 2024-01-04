import unicodedata
from datetime import datetime, timezone
from random import choice
from typing import Optional

import requests
from bs4 import BeautifulSoup
from faker import Faker
from us.states import STATES_AND_TERRITORIES

from tollway.constants import STATE_NAMES, TIMESTAMP_FORMAT, TOLLWAYS_URL


def create_vehicle(fake: Faker) -> dict:

    vehicle = {key.lower(): value for key, value in fake.vehicle_object().items()}
    vehicle["year"] = str(vehicle["year"])
    vehicle["license_plate"] = fake.license_plate()
    vehicle["vin"] = fake.vin()
    vehicle["state"] = choice(STATES_AND_TERRITORIES).abbr
    vehicle["primary_color"] = fake.color_name()

    return vehicle


def get_tollways(html: Optional[requests.Response] = None) -> dict:
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
                    [unicodedata.normalize("NFKD", td.text.strip()) for tr in sibling.find_all("tr") if (td := tr.find("td")) is not None]
                )
            # don't include tables after the next h2
            if sibling.name == "h2":
                break

        tables.append(tolls)

    united_states_tollways = {state: tolls for state, tolls in zip(states, tables) if tolls}
    return united_states_tollways


def create_tollway(tollways: dict) -> tuple[str, str]:
    state = choice(list(tollways.keys()))
    name = choice(tollways[state])
    return state, name


def create_message(vehicle: dict[str, str], tollway: tuple[str, str]) -> dict[str, str]:
    state_tollway = {
        "tollway_state": tollway[0],
        "tollway_name": tollway[1],
    }
    vehicle.update(state_tollway)
    vehicle["timestamp"] = datetime.now(tz=timezone.utc).strftime(TIMESTAMP_FORMAT)
    return vehicle
