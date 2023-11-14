def test_create_vehicle(setup, vehicle):
    assert len(vehicle) == 8
    assert isinstance(vehicle.get("year"), int)
    (vehicle_values_type,) = set([type(value).__name__ for value in vehicle.values()][1:])
    assert vehicle_values_type  == "str"
    assert vehicle.get("state") in [state.abbr for state in setup.get("states")]


def test_get_tollways(tollways):
    states = [state for state in tollways.keys()]
    assert len(states) == 29
    assert len(tollways.get("Alabama")) == 4
    assert len(tollways.get("California")) == 16
    assert len(tollways.get("Colorado")) == 8
    assert len(tollways.get("Delaware")) == 3
    assert len(tollways.get("Florida")) == 35
    assert len(tollways.get("Georgia")) == 4
    assert len(tollways.get("Illinois")) == 6
    assert len(tollways.get("Indiana")) == 1
    assert len(tollways.get("Kansas")) == 1
    assert len(tollways.get("Louisiana")) == 1
    assert len(tollways.get("Maine")) == 1
    assert len(tollways.get("Maryland")) == 3
    assert len(tollways.get("Massachusetts")) == 1
    assert len(tollways.get("Minnesota")) == 4
    assert len(tollways.get("New Hampshire")) == 3
    assert len(tollways.get("New Jersey")) == 5
    assert len(tollways.get("New York")) == 3
    assert len(tollways.get("North Carolina")) == 3
    assert len(tollways.get("Ohio")) == 1
    assert len(tollways.get("Oklahoma")) == 11
    assert len(tollways.get("Pennsylvania")) == 6
    assert len(tollways.get("Puerto Rico")) == 8
    assert len(tollways.get("Rhode Island")) == 5
    assert len(tollways.get("South Carolina")) == 1
    assert len(tollways.get("Texas")) == 38
    assert len(tollways.get("Utah")) == 2
    assert len(tollways.get("Virginia")) == 12
    assert len(tollways.get("Washington")) == 2
    assert len(tollways.get("West Virginia")) == 1


def test_create_tollway(tollways, get_tollway):
    state, name = get_tollway
    assert name in tollways[state]