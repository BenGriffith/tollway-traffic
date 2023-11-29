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
    ],
)
def test_app_inputs(test_input, expected):
    result = runner.invoke(app, test_input)
    assert result.exit_code == expected
