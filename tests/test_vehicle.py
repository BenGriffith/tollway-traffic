def test_create_vehicle(setup, vehicle):
    assert len(vehicle) == 8
    assert isinstance(vehicle.get("year"), int)
    (vehicle_values_type,) = set([type(value).__name__ for value in vehicle.values()][1:])
    assert vehicle_values_type  == "str"
    assert vehicle.get("state") in [state.abbr for state in setup.get("states")]


def test_get_tollways(tollways, vehicle_constants):
    states = [state for state in tollways.keys()]
    assert len(states) == vehicle_constants.get("STATES")
    assert len(tollways.get("Alabama")) == vehicle_constants.get("ALABAMA")
    assert len(tollways.get("California")) == vehicle_constants.get("CALIFORNIA")
    assert len(tollways.get("Colorado")) == vehicle_constants.get("COLORADO")
    assert len(tollways.get("Delaware")) == vehicle_constants.get("DELAWARE")
    assert len(tollways.get("Florida")) == vehicle_constants.get("FLORIDA")
    assert len(tollways.get("Georgia")) == vehicle_constants.get("GEORGIA")
    assert len(tollways.get("Illinois")) == vehicle_constants.get("ILLINOIS")
    assert len(tollways.get("Indiana")) == vehicle_constants.get("INDIANA")
    assert len(tollways.get("Kansas")) == vehicle_constants.get("KANSAS")
    assert len(tollways.get("Louisiana")) == vehicle_constants.get("LOUISIANA")
    assert len(tollways.get("Maine")) == vehicle_constants.get("MAINE")
    assert len(tollways.get("Maryland")) == vehicle_constants.get("MARYLAND")
    assert len(tollways.get("Massachusetts")) == vehicle_constants.get("MASSACHUSETTS")
    assert len(tollways.get("Minnesota")) == vehicle_constants.get("MINNESOTA")
    assert len(tollways.get("New Hampshire")) == vehicle_constants.get("NEW HAMPSHIRE")
    assert len(tollways.get("New Jersey")) == vehicle_constants.get("NEW JERSEY")
    assert len(tollways.get("New York")) == vehicle_constants.get("NEW YORK")
    assert len(tollways.get("North Carolina")) == vehicle_constants.get("NORTH CAROLINA")
    assert len(tollways.get("Ohio")) == vehicle_constants.get("OHIO")
    assert len(tollways.get("Oklahoma")) == vehicle_constants.get("OKLAHOMA")
    assert len(tollways.get("Pennsylvania")) == vehicle_constants.get("PENNSYLVANIA")
    assert len(tollways.get("Puerto Rico")) == vehicle_constants.get("PUERTO RICO")
    assert len(tollways.get("Rhode Island")) == vehicle_constants.get("RHODE ISLAND")
    assert len(tollways.get("South Carolina")) == vehicle_constants.get("SOUTH CAROLINA")
    assert len(tollways.get("Texas")) == vehicle_constants.get("TEXAS")
    assert len(tollways.get("Utah")) == vehicle_constants.get("UTAH")
    assert len(tollways.get("Virginia")) == vehicle_constants.get("VIRGINIA")
    assert len(tollways.get("Washington")) == vehicle_constants.get("WASHINGTON")
    assert len(tollways.get("West Virginia")) == vehicle_constants.get("WEST VIRGINIA")


def test_create_tollway(tollways, get_tollway):
    state, name = get_tollway
    assert name in tollways[state]


def test_create_payload(payload, vehicle_constants):
    assert len(payload) == vehicle_constants.get("PAYLOAD_LENGTH")