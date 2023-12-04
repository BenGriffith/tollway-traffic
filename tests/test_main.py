import pytest
from typer.testing import CliRunner

from tollway.__main__ import app

runner = CliRunner()


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (["--total-events", 10, "--event-rate", 0.01], 0),
        (["--total-events", "ten"], 2),  # invalid type
        (["--total-events", -10], 2),  # callback
        (["--event-rate", -1], 2),  # callback
        (["--output-file", "True"], 2),  # invalid type
        (["--output-filename", "invalid-format.csv"], 2),  # invalid format
        (["--output-filename", "invalid-format.jsn"], 2),  # invalid format
        (["--date-variation", "--include-late", "--include-duplicate"], 2),  # invalid combination
        (["--date-variation", "--include-late"], 2),  # invalid combination
        (["--date-variation", "--include-duplicate"], 2),  # invalid combination
        (["--date-variation"], 0),
        (["--include-late"], 0),
        (["--include-duplicate"], 0),
        (["--include-late", "--include-duplicate"], 0),  # valid combination
    ],
)
def test_app_inputs(test_input, expected):
    result = runner.invoke(app, test_input)
    assert result.exit_code == expected
