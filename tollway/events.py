import logging
import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, Union

from faker import Faker
from google.pubsub_v1 import PublisherClient

from tollway.constants import (
    DUPLICATE_RATE,
    LATE_EVENT_RATE,
    TIME_UNIT,
    TIMESTAMP_FORMAT,
)
from tollway.utils import EventsLog, encode_message, future_callback
from tollway.vehicle import create_message, create_tollway, create_vehicle


class EventProcessor(ABC):
    def __init__(self, events_log: EventsLog, publisher: PublisherClient, topic_path: Optional[str]) -> None:
        self.events_log = events_log
        self.publisher = publisher
        self.topic_path = topic_path
        self.processed = False

    def publish_event(self, event_message: dict[str, str], pubsub_logger: logging.Logger) -> None:
        if self.publisher and self.topic_path:
            data = encode_message(message=event_message)
            future = self.publisher.publish(topic=self.topic_path, data=data)
            future.add_done_callback(future_callback(logger=pubsub_logger))

    def add_to_events_log(self, event_message: dict[str, Union[str, bool]]) -> None:
        self.events_log["all_events"].append(event_message)

    @abstractmethod
    def create_event(self) -> dict[str, Union[str, bool]]:
        """Implement in subclass to create event"""

    @abstractmethod
    def process_event(self, pubsub_logger: logging.Logger) -> tuple[EventsLog, bool]:
        """Implement in subclass to process event"""


class LateEventProcessor(EventProcessor):
    def __init__(
        self,
        events_log: EventsLog,
        publisher: PublisherClient,
        topic_path: Optional[str],
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

    def process_event(self, pubsub_logger):
        for time_interval, late_events in self.events_log["late_events"].items():
            self.time_unit = time_interval
            if len(late_events) == LATE_EVENT_RATE[self.time_unit]:
                late_event = self.create_event()
                self.publish_event(event_message=late_event, pubsub_logger=pubsub_logger)
                late_event["is_late"] = self.time_unit
                self.add_to_events_log(event_message=late_event)
                self.events_log["late_events"][self.time_unit] = []
                self.processed = True
        return self.events_log, self.processed


class DuplicateEventProcessor(EventProcessor):
    def __init__(self, events_log, publisher, topic_path) -> None:
        super().__init__(events_log, publisher, topic_path)

    def create_event(self):
        return random.choice(self.events_log["past_events"])

    def process_event(self, pubsub_logger):
        """
        For processing of duplicate events, previous events are temporarily stored
        in events_log["past_events"]. If the number of previous events is equal to
        DUPLICATE_RATE, then the following occurs:

        1. Randomly select a previous event to serve as the duplicate
        2. If pubsub is enabled, push the message to pubsub
        3. ...
        """
        if len(self.events_log["past_events"]) == DUPLICATE_RATE:
            duplicate_event = self.create_event()
            self.publish_event(event_message=duplicate_event, pubsub_logger=pubsub_logger)
            duplicate_event["is_duplicate"] = True
            self.add_to_events_log(event_message=duplicate_event)
            self.events_log["past_events"] = []
            self.processed = True
        return self.events_log, self.processed
