def test_create_vehicle(setup, vehicle):
    assert len(vehicle) == 8
    assert isinstance(vehicle.get("year"), int)
    (vehicle_values_type,) = set([type(value).__name__ for value in vehicle.values()][1:])
    assert vehicle_values_type  == "str"
    assert vehicle.get("state") in [state.abbr for state in setup.get("states")]


def test_get_tollways():
    pass