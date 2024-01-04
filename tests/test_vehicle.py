import pytest


def test_create_vehicle(setup, vehicle):
    assert len(vehicle) == 8
    (vehicle_values_type,) = set([type(value).__name__ for value in vehicle.values()][1:])
    assert vehicle_values_type == "str"
    assert vehicle.get("state") in [state.abbr for state in setup.get("states")]


def test_get_states(tollways):
    states = [state for state in tollways.keys()]
    assert len(states) == 29


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("Alabama", 4),
        ("California", 17),
        ("Colorado", 8),
        ("Delaware", 3),
        ("Florida", 35),
        ("Georgia", 4),
        ("Illinois", 6),
        ("Indiana", 1),
        ("Kansas", 1),
        ("Louisiana", 1),
        ("Maine", 1),
        ("Maryland", 3),
        ("Massachusetts", 1),
        ("Minnesota", 4),
        ("New Hampshire", 3),
        ("New Jersey", 5),
        ("New York", 3),
        ("North Carolina", 3),
        ("Ohio", 1),
        ("Oklahoma", 11),
        ("Pennsylvania", 6),
        ("Puerto Rico", 8),
        ("Rhode Island", 5),
        ("South Carolina", 1),
        ("Texas", 38),
        ("Utah", 2),
        ("Virginia", 12),
        ("Washington", 2),
        ("West Virginia", 1),
    ],
)
def test_get_state_tollways(tollways, test_input, expected):
    assert len(tollways.get(test_input)) == expected


def test_create_tollway(tollways, get_tollway):
    state, name = get_tollway
    assert name in tollways[state]


def test_create_message(message):
    assert len(message) == 11
