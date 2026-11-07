import plotly.graph_objects as go


def create_temperature_chart(weather):
    fig = go.Figure()

    dates = weather["daily"]["time"]
    max_temps = weather["daily"]["temperature_2m_max"]
    min_temps = weather["daily"]["temperature_2m_min"]

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=max_temps,
            mode="lines+markers",
            name="Max temperature",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=min_temps,
            mode="lines+markers",
            name="Min temperature",
        )
    )

    return fig.to_html(full_html=False, include_plotlyjs="cdn")
