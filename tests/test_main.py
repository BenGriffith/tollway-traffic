import pytest
from typer.testing import CliRunner

from tollway.__main__ import app

runner = CliRunner()


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (["--total-events", 10, "--event-rate", 0.01], 0),
        pytest.param(["--total-events", "ten"], 2, id="total_events_invalid_type"),
        pytest.param(["--total-events", -10], 2, id="total_events_callback"),
        pytest.param(["--event-rate", -1], 2, id="event_rate_callback"),
        pytest.param(["--output-file", "True"], 2, id="output_file_invalid_type"),
        pytest.param(["--output-filename", "invalid-format.csv"], 2, id="output_filename_invalid_csv"),
        pytest.param(["--output-filename", "invalid-format.jsn"], 2, id="output_filename_invalide_json"),
        pytest.param(["--date-variation", "--include-late", "--include-duplicate"], 2, id="date_variation_invalid_combo"),
        pytest.param(["--date-variation", "--include-late"], 2, id="date_variation_late_combo"),
        pytest.param(["--date-variation", "--include-duplicate"], 2, id="date_variation_duplicate_combo"),
        (["--date-variation"], 0),
        (["--include-late"], 0),
        (["--include-duplicate"], 0),
        pytest.param(["--include-late", "--include-duplicate"], 0, id="valid_combination"),
    ],
)
def test_app_inputs(test_input, expected):
    result = runner.invoke(app, test_input)
    assert result.exit_code == expected
