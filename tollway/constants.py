from enum import Enum

from us.states import STATES_AND_TERRITORIES

from tollway.utils import get_envs

STATE_NAMES = [state.name for state in STATES_AND_TERRITORIES]
URL_PATH = "wiki/List_of_toll_roads_in_the_United_States"
TOLLWAYS_URL = f"https://en.wikipedia.org/{URL_PATH}"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f %z"
DUPLICATE_RATE = get_envs("duplicate")
ALL_EVENTS_COUNT = get_envs("all")
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
    "seconds": get_envs("seconds"),
    "minutes": get_envs("minutes"),
    "hours": get_envs("hours"),
    "days": get_envs("days"),
}


TIME_UNIT = {
    "seconds": {"min": 5, "max": 30},
    "minutes": {"min": 1, "max": 59},
    "hours": {"min": 1, "max": 23},
    "days": {"min": 1, "max": 5},
}
