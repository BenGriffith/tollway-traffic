from pathlib import Path

import typer

from tollway.constants import FILE_SUFFIX


def total_event_callback(total_events: int):
    if total_events <= 0:
        raise typer.BadParameter("--total-events must be greater than 0")
    return total_events


def event_rate_callback(event_rate: float):
    if event_rate <= 0:
        raise typer.BadParameter("--event-rate must be greater than 0")
    return event_rate


def filename_callback(filename: str):
    path = Path(filename.lower())
    if FILE_SUFFIX not in path.suffix:
        raise typer.BadParameter("--output-filename must use json format")
    return filename


def behavior_callback(ctx: typer.Context, include_duplicate: bool):
    date_variation = ctx.params.get("date_variation")
    include_late = ctx.params.get("include_late")

    if date_variation:
        if include_late or include_duplicate:
            raise typer.BadParameter(
                "when --date-variation is True --include-late and --include-duplicate must be False"
            )
