import pytest

from cities import is_valid_city


def test_valid_city():
    assert is_valid_city("Stockholm")


def test_invalid_city():
    assert not is_valid_city("London")


@pytest.mark.parametrize(
    "city, expected",
    [
        ("Stockholm", True),
        ("London", False),
    ],
)
def test_city_validation(city, expected):
    assert is_valid_city(city) == expected
