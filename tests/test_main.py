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
        pytest.param(["--date-variation", "--include-late", "--include-duplicate"], 2, id="fail_date_variation"),
        pytest.param(["--date-variation", "--include-late"], 2, id="fail_date_variation_include_late"),
        pytest.param(["--date-variation", "--include-duplicate"], 2, id="fail_date_variation_include_duplicate"),
        pytest.param(["--date-variation"], 0, id="pass_date_variation"),
        pytest.param(["--include-late"], 0, id="pass_include_late"),
        pytest.param(["--include-duplicate"], 0, id="pass_include_duplicate"),
        pytest.param(["--include-late", "--include-duplicate"], 0, id="pass_include_late_include_duplicate"),
    ],
)
def test_app_inputs(test_input, expected):
    result = runner.invoke(app, test_input)
    assert result.exit_code == expected
