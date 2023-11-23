from pathlib import Path

import typer

from tollway.constants import FILE_SUFFIX


def te_callback(total_events_value: int):
    if total_events_value <= 0:
        raise typer.BadParameter("--total-events must be greater than 0")
    return total_events_value


def er_callback(event_rate_value: float):
    if event_rate_value <= 0:
        raise typer.BadParameter("--event-rate must be greater than 0")
    return event_rate_value


def of_callback(filename_value: str):
    path = Path(filename_value.lower())
    if FILE_SUFFIX not in path.suffix:
        raise typer.BadParameter("--output-filename must use json format")
    return filename_value
