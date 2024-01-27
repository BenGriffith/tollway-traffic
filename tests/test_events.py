from tollway.constants import TIME_UNIT


def test_create_late_events(original_and_late_events_timestamps):
    events = original_and_late_events_timestamps
    seconds_difference = abs(events["seconds"]["original"] - events["seconds"]["late"]).seconds
    minutes_difference = abs(events["minutes"]["original"] - events["minutes"]["late"]).seconds // 60
    hours_difference = abs(events["hours"]["original"] - events["hours"]["late"]).seconds // 3600
    days_difference = abs(events["days"]["original"] - events["days"]["late"]).days

    assert TIME_UNIT["seconds"]["min"] <= seconds_difference <= TIME_UNIT["seconds"]["max"]
    assert TIME_UNIT["minutes"]["min"] <= minutes_difference <= TIME_UNIT["minutes"]["max"]
    assert TIME_UNIT["hours"]["min"] <= hours_difference <= TIME_UNIT["hours"]["max"]
    assert TIME_UNIT["days"]["min"] <= days_difference <= TIME_UNIT["days"]["max"]


def test_create_duplicate_event(duplicate_event, past_events):
    assert duplicate_event in past_events["past_events"]
