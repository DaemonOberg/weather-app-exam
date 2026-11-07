# Weather App

A weather forecast web application built with Python and Flask. The application retrieves live weather data from the Open-Meteo API and displays current weather conditions, a three-day forecast, and an interactive temperature chart.

The project was developed using Test-Driven Development (TDD), automated testing with pytest, and code quality checks with Ruff.

## Features

- View weather forecasts for five Swedish cities: Stockholm, Göteborg, Malmö, Umeå, and Kiruna.
- Display current temperature and wind speed.
- View a three-day forecast with maximum temperature, minimum temperature, and precipitation.
- Explore an interactive Plotly chart comparing maximum and minimum temperatures.
- Validate selected cities and handle API errors.
- Display a custom 404 error page.
- Styled interface using HTML, CSS, and Jinja2 templates.

## Technologies

- **Python** – Application logic
- **Flask** – Web framework and routing
- **Open-Meteo API** – Weather data
- **Requests** – HTTP requests
- **Plotly** – Interactive temperature visualization
- **HTML, CSS, Jinja2** – User interface
- **pytest** – Automated testing
- **Ruff** – Linting and code formatting
- **Git and GitHub** – Version control

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/DaemonOberg/weather-app-exam.git
cd weather-app-exam
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

For development and testing, also install:

```bash
python -m pip install -r requirements-dev.txt
```

## Running the Application

Start the Flask development server:

```bash
python -m flask --app app run --debug
```

Open your browser and visit:

http://127.0.0.1:5000

Select a city to view its weather forecast.

An internet connection is required to retrieve weather information and load Plotly's JavaScript library from its CDN.

## Running Tests

The application uses pytest for automated testing.

Run all tests:

```bash
python -m pytest -v
```

Run a specific test file:

```bash
python -m pytest tests/test_weather_api.py -v
```

The test suite covers:

- Flask routes and HTTP status codes
- City validation
- Successful weather API responses
- API timeouts and HTTP errors
- Missing or invalid weather data, including invalid temperature types
- Plotly chart generation
- Integration of the temperature chart into the weather page

**Latest verified result: 40 tests passed.**

## Code Quality

Ruff is used for linting and automatic code formatting to maintain consistent code quality throughout the project.

### Linting

Check the code for potential issues:

```bash
python -m ruff check .
```

### Formatting

Automatically format the Python code:

```bash
python -m ruff format .
```

Check formatting without modifying any files:

```bash
python -m ruff format --check .
```

### Verification

Before committing changes, I run pytest, Ruff linting, and formatting checks:

```bash
python -m pytest -v
python -m ruff check .
python -m ruff format --check .
```

This helps ensure that the tests pass and the code follows consistent formatting standards.

## Test-Driven Development (TDD)

The project follows the RED → GREEN → REFACTOR workflow.

1. **RED:** Write a test that fails because the required functionality does not exist yet.
2. **GREEN:** Implement the functionality needed to make the test pass.
3. **REFACTOR:** Improve the implementation while keeping the tests passing.

Git commits document the development process, including separate RED, GREEN, and REFACTOR stages where applicable.

## Project Structure

```text
weather-app-exam/
├── app.py
├── weather_api.py
├── cities.py
├── charts.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── weather.html
│   ├── info.html
│   └── 404.html
├── static/
│   └── css/
│       └── style.css
└── tests/
    ├── test_app.py
    ├── test_weather_api.py
    ├── test_cities.py
    └── test_charts.py
```

## Error Handling

The application validates city selections before requesting weather data.

It also handles network-related errors, invalid API responses, and incomplete forecast information.

If weather data cannot be retrieved, the application returns an HTTP 503 response with a user-friendly message.

Invalid or missing city selections return HTTP 400, and unknown pages display a custom HTTP 404 page.

## Questions and Answers

### 1. Why do you mock API calls in your tests, and what would happen if you did not?

**Svenska: Varför mockar du API-anrop i dina tester, och vad skulle hända om du inte gjorde det?**

I mock API calls to make my tests faster and more reliable without depending on an internet connection or the availability of the weather API. In `tests/test_weather_api.py`, I use `patch("weather_api.requests.get")` to simulate API responses, including errors and timeouts. Without mocking, the tests could fail because of network problems or changes in the external API, even if my own code works correctly.

**Svensk översättning:**

Jag mockar API-anrop för att göra mina tester snabbare och mer pålitliga utan att vara beroende av en internetanslutning eller att väder-API:et är tillgängligt. I `tests/test_weather_api.py` använder jag `patch("weather_api.requests.get")` för att simulera API-svar, inklusive fel och timeout. Utan mockning skulle testerna kunna misslyckas på grund av nätverksproblem eller förändringar i det externa API:et, även om min egen kod fungerar korrekt.

### 2. What do `timeout` and `raise_for_status()` do, and why are they needed?

**Svenska: Vad gör `timeout` och `raise_for_status()`, och varför behövs de?**

In `weather_api.py`, I use `timeout=5` in `requests.get()` to prevent the application from waiting indefinitely for an API response. I also use `response.raise_for_status()` to raise an exception when the server returns an HTTP error, such as 404 or 500. Both help the application handle network problems and API failures instead of continuing with invalid data.

**Svensk översättning:**

I `weather_api.py` använder jag `timeout=5` i `requests.get()` för att förhindra att applikationen väntar hur länge som helst på ett API-svar. Jag använder också `response.raise_for_status()` för att skapa ett undantag (exception) när servern returnerar ett HTTP-fel, exempelvis 404 eller 500. Båda hjälper applikationen att hantera nätverksproblem och API-fel i stället för att fortsätta med ogiltiga data.

### 3. How do templates work in Jinja2? Explain using examples from your own templates.

**Svenska: Hur fungerar mallar i Jinja2? Förklara med exempel från dina egna mallar.**

Jinja2 templates allow me to combine HTML with dynamic data sent from Flask using `render_template()` in `app.py`. In `weather.html`, I use `{{ city }}` to display the selected city and a `{% for %}` loop to generate the three-day forecast table. I also use `{% extends "base.html" %}` to reuse the common page layout, and `{{ chart_html | safe }}` to display the Plotly chart.

**Svensk översättning:**

Jinja2-mallar gör att jag kan kombinera HTML med dynamiska data som skickas från Flask genom `render_template()` i `app.py`. I `weather.html` använder jag `{{ city }}` för att visa den valda staden och en `{% for %}`-loop för att skapa tabellen med tredagarsprognosen. Jag använder också `{% extends "base.html" %}` för att återanvända sidans gemensamma layout och `{{ chart_html | safe }}` för att visa Plotly-diagrammet.

### 4. What is a fixture, and which one do you use?

**Svenska: Vad är en fixture, och vilken använder du?**

A fixture in pytest provides reusable test data or setup code for multiple tests. In my `tests/test_app.py`, I use two fixtures: `client` and `weather_data`, both defined with `@pytest.fixture`. The `client` fixture uses `app.test_client()` to simulate HTTP requests to my Flask application, while `weather_data` provides predefined weather data for testing without calling the real API. I use these fixtures in tests such as `test_weather_valid_city` and `test_weather_page_contains_chart`.

**Svensk översättning:**

En fixture i pytest är en funktion som tillhandahåller återanvändbara testdata eller förberedelser för flera tester. I min `tests/test_app.py` använder jag två fixtures: `client` och `weather_data`, som båda definieras med `@pytest.fixture`. Fixturen `client` använder `app.test_client()` för att simulera HTTP-anrop till min Flask-applikation, medan `weather_data` innehåller fördefinierade väderdata så att jag kan testa utan att anropa det riktiga API:et. Jag använder dessa fixtures i tester som `test_weather_valid_city` och `test_weather_page_contains_chart`.

## Weather Data Source

Weather forecasts are provided by the [Open-Meteo API](https://open-meteo.com/).

Weather information depends on the availability and accuracy of the external API.

## License and Attribution

Weather data is provided by Open-Meteo.

The application's information page includes a Creative Commons license reference. See the information page for attribution details.
