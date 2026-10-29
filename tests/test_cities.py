from cities import is_valid_city


def test_valid_city():
    assert is_valid_city("Stockholm")


def test_invalid_city():
    assert not is_valid_city("London")
