import pytest

from cities import is_valid_city


@pytest.mark.parametrize(
    "city, expected",
    [
        ("Stockholm", True),
        ("London", False),
    ],
)
def test_city_validation(city, expected):
    assert is_valid_city(city) == expected
