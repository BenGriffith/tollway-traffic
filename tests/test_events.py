from tollway.events import create_late_event, create_duplicate_event


def test_create_late_event(past_events_timestamps, setup, get_tollway):
    late_event = create_late_event(events_log=past_events_timestamps, fake=setup.get("faker"), tollway=get_tollway)
    assert late_event.get("timestamp") in past_events_timestamps.get("past_events_timestamps")


def test_create_duplicate_event(past_events):
    duplicate_event = create_duplicate_event(events_log=past_events)
    assert duplicate_event in past_events.get("past_events")