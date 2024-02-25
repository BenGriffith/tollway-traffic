from enum import Enum

from us.states import STATES_AND_TERRITORIES

from tollway.utils import get_config_with_default

STATE_NAMES = [state.name for state in STATES_AND_TERRITORIES]
URL_PATH = "wiki/List_of_toll_roads_in_the_United_States"
TOLLWAYS_URL = f"https://en.wikipedia.org/{URL_PATH}"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f %z"
DUPLICATE_RATE = get_config_with_default(key="DUPLICATE_RATE", default_value=50)
ALL_EVENTS_COUNT = get_config_with_default(key="ALL_EVENTS_COUNT", default_value=250)
FILENAME = "tollway-traffic.json"
FILE_SUFFIX = "json"


class Help(Enum):
    TOTAL_EVENTS = "number of events to generate"
    EVENT_RATE = "rate at which events should be created"
    OUTPUT_FILE = "write all events to a local file/log"
    OUTPUT_FILENAME = "provide your own JSON filename"
    INCLUDE_LATE_SECONDS = "generate late events by seconds"
    INCLUDE_LATE_MINUTES = "generate late events by minutes"
    INCLUDE_LATE_HOURS = "generate late events by hours"
    INCLUDE_LATE_DAYS = "generate late events by days"
    INCLUDE_DUPLICATE = "generate duplicate events"
    PUBSUB = "enable PubSub functionality"


LATE_EVENT_RATE = {
    "seconds": get_config_with_default(key="LATE_SECONDS_RATE", default_value=10),
    "minutes": get_config_with_default(key="LATE_MINUTES_RATE", default_value=20),
    "hours": get_config_with_default(key="LATE_HOURS_RATE", default_value=30),
    "days": get_config_with_default(key="LATE_DAYS_RATE", default_value=100),
}


TIME_UNIT = {
    "seconds": {"min": 5, "max": 30},
    "minutes": {"min": 1, "max": 59},
    "hours": {"min": 1, "max": 23},
    "days": {"min": 1, "max": 5},
}
