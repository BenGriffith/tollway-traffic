from datetime import datetime, timezone

from tollway.utils import get_date_variation
from tollway.constants import TIMESTAMP_FORMAT


def test_date_variation():
    timestamp = datetime.now(tz=timezone.utc)
    updated_timestamp = get_date_variation(timestamp=timestamp.strftime(TIMESTAMP_FORMAT))
    timestamp_difference = timestamp - datetime.strptime(updated_timestamp, TIMESTAMP_FORMAT)
    assert timestamp_difference.days in [1, 2, 3]