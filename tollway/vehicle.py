from random import choice
from collections import deque

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


def _num_of_tables_between_states(soup: BeautifulSoup) -> dict:
    states = {}
    table_count_between_states = 0
    state_name = ""
    for row in soup.contents[0]:
        if not isinstance(row, Tag):
            continue

        if isinstance(row, Tag) and row.name == "h2" and row.span.string in STATE_NAMES:
            state_name = row.span.string
            table_count_between_states = 0

        if isinstance(row, Tag) and row.name == "table" and row["class"][0] == "wikitable" and state_name != "":
            table_count_between_states += 1
            states[state_name] = table_count_between_states

    return states


def _state_tollways(soup: BeautifulSoup) -> list:
    names = []

    for table in soup.find_all("table", class_="wikitable"):
        table_rows = table.tbody.find_all("tr")[1:]
        state_tollways = []
        for table_row in table_rows:
            for tag in table_row.find_all("a"):
                if tag.string is None:
                    continue
                state_tollways.append(tag.string)
                break
        names.append(state_tollways)
    
    return names


def get_tollways() -> dict:
    tollways_html = requests.get(TOLLWAYS_URL)
    wikipedia_soup = BeautifulSoup(markup=tollways_html.text, features="html.parser")

    tollway_content = wikipedia_soup.find("div", class_="mw-parser-output")
    tollway_subsection = BeautifulSoup(markup=str(tollway_content), features="html.parser")

    num_of_tables_between_states = _num_of_tables_between_states(soup=tollway_subsection)
    state_tollways = deque(_state_tollways(soup=tollway_subsection))

    united_states_tollways = {}
    for state_name, table_count in num_of_tables_between_states.items():

        merge_tollway_tables = []
        for _ in range(table_count):
            merge_tollway_tables.extend(state_tollways.popleft())

        united_states_tollways[state_name] = set(merge_tollway_tables)
        merge_tollway_tables = []

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