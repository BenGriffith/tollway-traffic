from random import choice

import requests
from bs4 import BeautifulSoup, Tag
from faker import Faker
from faker_vehicle import VehicleProvider
from us.states import STATES


TOLLWAYS_URL = "https://en.wikipedia.org/wiki/List_of_toll_roads_in_the_United_States"


def create_vehicle(fake: Faker) -> dict:
    
    vehicle = {f"{key.lower()}": value for key, value in fake.vehicle_object().items()}
    vehicle["license_plate"] = fake.license_plate()
    vehicle["vin"] = fake.vin()
    vehicle["state"] = choice(STATES).abbr
    vehicle["primary_color"] = fake.color_name()

    return vehicle


def _states():
    pass


def _state_tollways():
    pass


def tollways() -> list[str]:
    tollways_html = requests.get(TOLLWAYS_URL)
    wikipedia_soup = BeautifulSoup(markup=tollways_html.text, features="html.parser")

    tollway_content = wikipedia_soup.find("div", class_="mw-parser-output")
    tollway_subsection = BeautifulSoup(markup=str(tollway_content), features="html.parser")

    state_names = [row.span.string for row in tollway_subsection.find_all("h2")]

    # process tables in state subsection

    # for row in tollway_subsection.find_all("h2"):
    #     row


    # subsection_tables = tollway_subsection.find_all("table", class_="wikitable")
    # names = []
    # for table in subsection_tables:
    #     table_rows = table.tbody.find_all("tr")[1:]

    #     state_tollways = []
    #     for _ in table_rows:
    #         state_tollways.append(_.td.a.string)
    #     names.append(state_tollways)

    # h2 -> state name
    # search for wikitable and process all until next h2

    state_managed_table_count = {}
    table_count = 0
    state = ""
    for row in tollway_subsection.contents[0]:

        if isinstance(row, Tag) and row.name == "h2":
            state = row.span.string
            table_count = 0


        if isinstance(row, Tag) and row.name == "table":
            table_count += 1

            state_managed_table_count[state] = table_count
        
            # if h2:
            #     breakpoint()
    breakpoint()







def create_tollway(tollways: list[str]) -> dict:
    pass
    # vehicle["tollway"]
    # vehicle[""]


def create_message() -> None:
    pass
    

if __name__ == "__main__":
    # fake = Faker()
    # fake.add_provider(VehicleProvider)
    # vehicle = create_vehicle(fake=fake)
    tollways()