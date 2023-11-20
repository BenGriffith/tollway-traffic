from enum import Enum

from us.states import STATES_AND_TERRITORIES

STATE_NAMES = [state.name for state in STATES_AND_TERRITORIES]
URL_PATH = "wiki/List_of_toll_roads_in_the_United_States"
TOLLWAYS_URL = f"https://en.wikipedia.org/{URL_PATH}"
TIMESTAMP_FORMAT = "%Y-%m-%d %M:%H:%S.%f %z"
DATE_VARIATION_RATE = 3
INCLUDE_LATE_RATE = 20
INCLUDE_DUPLICATE_RATE = 50
ALL_EVENTS_COUNT = 250


class Help(Enum):
    TOTAL_EVENTS = "number of events to generate"
    EVENT_RATE = "rate at which events should be created"
    OUTPUT_FILE = "write all events to a local file/log"
    OUTPUT_FILENAME = "provide your own JSON filename"
    DATE_VARIATION = "'mini-batch' of messages with noticeably different dates"
    INCLUDE_LATE = "generate late events"
    INCLUDE_DUPLICATE = "generate duplicate events"
