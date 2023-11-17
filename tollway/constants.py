from us.states import STATES_AND_TERRITORIES

STATE_NAMES = [state.name for state in STATES_AND_TERRITORIES]
TOLLWAYS_URL = "https://en.wikipedia.org/wiki/List_of_toll_roads_in_the_United_States"
TIMESTAMP_FORMAT = "%Y-%m-%d %M:%H:%S.%f %Z"
DATE_VARIATION_RATE = 3
INCLUDE_LATE_RATE = 20
INCLUDE_DUPLICATE_RATE = 50
ALL_EVENTS_COUNT = 100