import pytest

from charts import create_temperature_chart


@pytest.fixture
def weather_data():
    return {
        "daily": {
            "time": ["2026-11-06", "2026-11-07", "2026-11-08"],
            "temperature_2m_max": [10.0, 11.0, 12.0],
            "temperature_2m_min": [2.0, 3.0, 4.0],
        }
    }


def test_create_temperature_chart_returns_html(weather_data):
    chart_html = create_temperature_chart(weather_data)

    assert isinstance(chart_html, str)


def test_create_temperature_chart_contains_both_lines(weather_data):
    chart_html = create_temperature_chart(weather_data)

    assert "Max temperature" in chart_html
    assert "Min temperature" in chart_html
