from datetime import datetime

from tollway.constants import TIME_UNIT, TIMESTAMP_FORMAT
from tollway.events import create_duplicate_event, create_late_event


def test_create_late_event_seconds(late_events, setup, tollways):
    late_event_ts = create_late_event(
        events_log=late_events, fake=setup.get("faker"), tollways=tollways, time_unit="seconds"
    )

    late_event_ts = datetime.strptime(late_event_ts["timestamp"], TIMESTAMP_FORMAT)
    for ts in late_events["late_events"]["seconds"]:
        current_event_ts = datetime.strptime(ts, TIMESTAMP_FORMAT)
        if late_event_ts.microsecond == current_event_ts.microsecond:
            difference_in_seconds = abs(current_event_ts - late_event_ts)
            assert TIME_UNIT["seconds"]["min"] <= difference_in_seconds.seconds <= TIME_UNIT["seconds"]["max"]


def test_create_late_event_minutes(late_events, setup, tollways):
    late_event_ts = create_late_event(
        events_log=late_events, fake=setup.get("faker"), tollways=tollways, time_unit="minutes"
    )

    late_event_ts = datetime.strptime(late_event_ts["timestamp"], TIMESTAMP_FORMAT)
    for ts in late_events["late_events"]["minutes"]:
        current_event_ts = datetime.strptime(ts, TIMESTAMP_FORMAT)
        if late_event_ts.microsecond == current_event_ts.microsecond:
            difference_in_minutes = abs(current_event_ts - late_event_ts).seconds // 60
            assert TIME_UNIT["minutes"]["min"] <= difference_in_minutes <= TIME_UNIT["minutes"]["max"]


def test_create_late_event_hours(late_events, setup, tollways):
    late_event_ts = create_late_event(
        events_log=late_events, fake=setup.get("faker"), tollways=tollways, time_unit="hours"
    )

    late_event_ts = datetime.strptime(late_event_ts["timestamp"], TIMESTAMP_FORMAT)
    for ts in late_events["late_events"]["hours"]:
        current_event_ts = datetime.strptime(ts, TIMESTAMP_FORMAT)
        if late_event_ts.microsecond == current_event_ts.microsecond:
            difference_in_minutes = abs(current_event_ts - late_event_ts).seconds // 3600
            assert TIME_UNIT["hours"]["min"] <= difference_in_minutes <= TIME_UNIT["hours"]["max"]


def test_create_late_event_days(late_events, setup, tollways):
    late_event_ts = create_late_event(
        events_log=late_events, fake=setup.get("faker"), tollways=tollways, time_unit="days"
    )

    late_event_ts = datetime.strptime(late_event_ts["timestamp"], TIMESTAMP_FORMAT)
    for ts in late_events["late_events"]["days"]:
        current_event_ts = datetime.strptime(ts, TIMESTAMP_FORMAT)
        if late_event_ts.microsecond == current_event_ts.microsecond:
            difference_in_days = abs(current_event_ts - late_event_ts).days
            assert TIME_UNIT["days"]["min"] <= difference_in_days <= TIME_UNIT["days"]["max"]


def test_create_duplicate_event(past_events):
    duplicate_event = create_duplicate_event(events_log=past_events)
    assert duplicate_event in past_events.get("past_events")
