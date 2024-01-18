from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from tollway.__main__ import app

runner = CliRunner()


@pytest.mark.parametrize(
    "test_input, expected",
    [
        pytest.param(["--total-events", 10, "--event-rate", 0.01], 0, id="pass_total_events_and_event_rate"),
        pytest.param(["--total-events", "ten"], 2, id="fail_total_events_type"),
        pytest.param(["--total-events", -10], 2, id="fail_total_events_lt_min"),
        pytest.param(["--event-rate", -1], 2, id="fail_event_rate_lt_min"),
        pytest.param(["--event-rate", 20], 2, id="fail_event_rate_gt_max"),
        pytest.param(["--output-file", "True"], 2, id="fail_output_file_type"),
        pytest.param(
            ["--total-events", 50, "--event-rate", 0.1, "--include-late-seconds"],
            0,
            id="pass_include_late_seconds",
        ),
        pytest.param(
            ["--total-events", 100, "--event-rate", 0.1, "--include-late-minutes"],
            0,
            id="pass_include_late_minutes",
        ),
        pytest.param(
            ["--total-events", 100, "--event-rate", 0.1, "--include-late-seconds", "--include-late-minutes"],
            0,
            id="pass_include_late_seconds_minutes",
        ),
        pytest.param(
            ["--total-events", 100, "--event-rate", 0.1, "--include-late-hours"],
            0,
            id="pass_include_late_hours",
        ),
        pytest.param(
            ["--total-events", 100, "--event-rate", 0.1, "--include-late-days"],
            0,
            id="pass_include_late_days",
        ),
        pytest.param(
            [
                "--total-events",
                100,
                "--event-rate",
                0.1,
                "--include-late-seconds",
                "--include-late-minutes",
                "--include-late-hours",
                "--include-late-days",
            ],
            0,
            id="pass_include_late_all",
        ),
    ],
)
def test_app_inputs(test_input, expected):
    result = runner.invoke(app, test_input)
    assert result.exit_code == expected


def test_output_file_format():
    test_input = ["--output-file", "--output-filename", "invalid-format.csv"]
    result = runner.invoke(app, test_input)
    assert result.exit_code == 2
    assert "--output-filename must use json format" in result.output


@patch("tollway.callbacks.PROJECT_ID", None)
def test_pubsub_no_project():
    test_input = ["--total-events", 10, "--event-rate", 0.1, "--pubsub"]
    result = runner.invoke(app, test_input)
    assert result.exit_code == 2
    assert "Please define PROJECT_ID in .env" in result.output


@patch("tollway.callbacks.PROJECT_ID", "my-project")
@patch("tollway.callbacks.TOPIC_ID", None)
def test_pubsub_no_topic():
    test_input = ["--total-events", 10, "--event-rate", 0.1, "--pubsub"]
    result = runner.invoke(app, test_input)
    assert result.exit_code == 2
    assert "Please define TOPIC_ID in .env" in result.output


def test_filename_output_file_disabled():
    test_input = ["--total-events", 10, "--event-rate", 0.1, "--output-filename", "myfile.json"]
    result = runner.invoke(app, test_input)
    assert result.exit_code == 2
    assert "--output-file must be enabled" in result.output
