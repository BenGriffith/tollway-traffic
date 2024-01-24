import random
from datetime import datetime, timedelta
from typing import Union

from faker import Faker
from google.pubsub_v1 import PublisherClient, Topic

from tollway.constants import (
    DUPLICATE_RATE,
    LATE_EVENT_RATE,
    TIME_UNIT,
    TIMESTAMP_FORMAT,
)
from tollway.utils import EventsLog, encode_message
from tollway.vehicle import create_message, create_tollway, create_vehicle


class EventProcessor:
    def __init__(self, events_log: EventsLog, publisher: PublisherClient, topic_path: Topic) -> None:
        self.events_log = events_log
        self.publisher = publisher
        self.topic_path = topic_path
        self.processed = False

    def publish_event(self, event_message: dict[str, str]) -> None:
        if self.publisher and self.topic_path:
            data = encode_message(message=event_message)
            future = self.publisher.publish(topic=self.topic_path, messages=data)

    def logging(self, event_message: dict[str, Union[str, bool]]) -> None:
        self.events_log["all_events"].append(event_message)

    def create_event(self) -> dict[str, Union[str, bool]]:
        raise NotImplementedError

    def process_event(self) -> tuple[EventsLog, bool]:
        raise NotImplementedError


class LateEventProcessor(EventProcessor):
    def __init__(
        self,
        events_log: EventsLog,
        publisher: PublisherClient,
        topic_path: Topic,
        fake: Faker,
        tollways: dict,
    ) -> None:
        super().__init__(events_log, publisher, topic_path)
        self.fake = fake
        self.tollways = tollways

    def _calculate_late_timestamp(self, time_unit: str, ts: str) -> str:
        random_integer = random.randint(TIME_UNIT[time_unit]["min"], TIME_UNIT[time_unit]["max"])
        current_timestamp = datetime.strptime(ts, TIMESTAMP_FORMAT)
        return (current_timestamp - timedelta(**{time_unit: random_integer})).strftime(TIMESTAMP_FORMAT)

    def create_event(self):
        past_timestamps = self.events_log["late_events"][self.time_unit]
        tollway = create_tollway(tollways=self.tollways)
        vehicle = create_vehicle(fake=self.fake)
        late_event_message = create_message(vehicle=vehicle, tollway=tollway)
        random_ts = random.choice(past_timestamps[slice(0, len(past_timestamps))])
        late_event_message["timestamp"] = self._calculate_late_timestamp(
            time_unit=self.time_unit, ts=random_ts
        )
        return late_event_message

    def process_event(self):
        for time_interval, late_events in self.events_log["late_events"].items():
            self.time_unit = time_interval
            if len(late_events) == LATE_EVENT_RATE:
                late_event = self.create_event()
                self.publish_event(event_message=late_event)
                late_event["is_late"] = self.time_unit
                self.logging(event_message=late_event)
                self.events_log["late_events"][self.time_unit] = []
                self.processed = True
        return self.events_log, self.processed


class DuplicateEventProcessor(EventProcessor):
    def __init__(self, events_log, publisher, topic_path) -> None:
        super().__init__(events_log, publisher, topic_path)

    def create_event(self):
        return random.choice(self.events_log["past_events"])

    def process_event(self):
        if len(self.events_log["past_events"] == DUPLICATE_RATE):
            duplicate_event = self.create_event()
            self.publish_event(event_message=duplicate_event)
            duplicate_event["is_duplicate"] = True
            self.logging(event_message=duplicate_event)
            self.events_log["past_events"] = []
            self.processed = True
        return self.events_log, self.processed
