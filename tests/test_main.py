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
        pytest.param(["--output-filename", "invalid-format.csv"], 2, id="fail_output_filename_csv"),
        pytest.param(["--output-filename", "invalid-format.jsn"], 2, id="fail_output_filename_json"),
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
