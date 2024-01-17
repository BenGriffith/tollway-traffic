from pathlib import Path

import typer

from tollway.constants import FILE_SUFFIX, PROJECT_ID, TOPIC_ID


def total_event_callback(total_events: int):
    if total_events <= 0:
        raise typer.BadParameter("--total-events must be greater than 0")
    return total_events


def event_rate_callback(event_rate: float):
    if event_rate <= 0:
        raise typer.BadParameter("--event-rate must be greater than 0")
    if event_rate > 10:
        raise typer.BadParameter("--event-rate must be less than 10")
    return event_rate


def filename_callback(filename: str):
    path = Path(filename.lower())
    if FILE_SUFFIX not in path.suffix:
        raise typer.BadParameter("--output-filename must use json format")
    return filename


def pubsub_callback(value):
    if value and PROJECT_ID is None:
        raise typer.BadParameter("Please define PROJECT_ID in .env")
    if value and TOPIC_ID is None:
        raise typer.BadParameter("Please define TOPIC_ID in .env")
    return value
