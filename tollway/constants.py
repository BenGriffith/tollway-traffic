from enum import Enum

from decouple import config
from us.states import STATES_AND_TERRITORIES

STATE_NAMES = [state.name for state in STATES_AND_TERRITORIES]
URL_PATH = "wiki/List_of_toll_roads_in_the_United_States"
TOLLWAYS_URL = f"https://en.wikipedia.org/{URL_PATH}"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f %z"
DATE_VARIATION_RATE = config("DATE_VARIATION_RATE", default=3, cast=int)
DATE_VARIATION_MIN = config("DATE_VARIATION_MIN", default=1, cast=int)
DATE_VARIATION_MAX = config("DATE_VARIATION_MAX", default=3, cast=int)
INCLUDE_LATE_RATE = config("INCLUDE_LATE_RATE", default=20, cast=int)
INCLUDE_DUPLICATE_RATE = config("INCLUDE_DUPLICATE_RATE", default=50, cast=int)
ALL_EVENTS_COUNT = config("ALL_EVENTS_COUNT", default=250, cast=int)
FILE_SUFFIX = "json"


class Help(Enum):
    TOTAL_EVENTS = "number of events to generate"
    EVENT_RATE = "rate at which events should be created"
    OUTPUT_FILE = "write all events to a local file/log"
    OUTPUT_FILENAME = "provide your own JSON filename"
    DATE_VARIATION = "'mini-batch' of messages with noticeably different dates"
    INCLUDE_LATE = "generate late events"
    INCLUDE_DUPLICATE = "generate duplicate events"
    PUBSUB = "enable PubSub functionality"
