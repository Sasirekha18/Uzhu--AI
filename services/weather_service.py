import requests
import pandas as pd


# ==========================================================
# Weather Code Mapping
# ==========================================================

WEATHER_CODES = {
    0: ("☀️", "Clear"),
    1: ("🌤", "Mainly Clear"),
    2: ("⛅", "Partly Cloudy"),
    3: ("☁️", "Cloudy"),

    45: ("🌫", "Fog"),
    48: ("🌫", "Dense Fog"),

    51: ("🌦", "Light Drizzle"),
    53: ("🌦", "Moderate Drizzle"),
    55: ("🌧", "Heavy Drizzle"),

    56: ("🌧", "Freezing Drizzle"),
    57: ("🌧", "Heavy Freezing Drizzle"),

    61: ("🌦", "Light Rain"),
    63: ("🌧", "Moderate Rain"),
    65: ("🌧", "Heavy Rain"),

    66: ("🌨", "Freezing Rain"),
    67: ("🌨", "Heavy Freezing Rain"),

    71: ("❄️", "Light Snow"),
    73: ("❄️", "Moderate Snow"),
    75: ("❄️", "Heavy Snow"),

    77: ("🌨", "Snow Grains"),

    80: ("🌦", "Rain Showers"),
    81: ("🌧", "Heavy Showers"),
    82: ("⛈", "Violent Showers"),

    85: ("🌨", "Snow Showers"),
    86: ("❄️", "Heavy Snow Showers"),

    95: ("⛈", "Thunderstorm"),
    96: ("⛈", "Thunderstorm with Hail"),
    99: ("⛈", "Severe Thunderstorm"),
}


# ==========================================================
# Weather Condition
# ==========================================================

def get_weather_condition(code):

    icon, text = WEATHER_CODES.get(
        code,
        ("🌤", "Unknown")
    )

    return f"{icon} {text}"


# ==========================================================
# Farming Activity
# ==========================================================

def get_farming_activity(rain):

    if rain >= 20:
        return "❌ Avoid Field Work"

    elif rain >= 10:
        return "🌧 Delay Irrigation"

    elif rain >= 5:
        return "🌱 Monitor Crops"

    elif rain >= 1:
        return "🚜 Fertilizer Application"

    else:
        return "💧 Irrigation Recommended"


# ==========================================================
# Weather Risk
# ==========================================================

def get_weather_risk(rain):

    if rain >= 20:
        return "🔴 High"

    elif rain >= 5:
        return "🟡 Medium"

    else:
        return "🟢 Low"


# ==========================================================
# Card Color
# ==========================================================

def get_card_color(rain):

    if rain >= 20:
        return "#B71C1C"

    elif rain >= 10:
        return "#EF6C00"

    elif rain >= 2:
        return "#1565C0"

    else:
        return "#2E7D32"


# ==========================================================
# Weather Forecast
# ==========================================================

def get_weather_forecast(lat, lon):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&current="
        "temperature_2m,"
        "relative_humidity_2m,"
        "wind_speed_10m,"
        "precipitation"

        "&daily="
        "temperature_2m_max,"
        "temperature_2m_min,"
        "precipitation_sum,"
        "wind_speed_10m_max,"
        "weathercode"

        "&forecast_days=7"
        "&timezone=auto"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

    except Exception:

        return None

    data = response.json()

    current = data["current"]

    daily = data["daily"]

    forecast = pd.DataFrame({

        "Date":
        daily["time"],

        "Max Temp":
        daily["temperature_2m_max"],

        "Min Temp":
        daily["temperature_2m_min"],

        "Rainfall":
        daily["precipitation_sum"],

        "Wind":
        daily["wind_speed_10m_max"],

        "WeatherCode":
        daily["weathercode"]

    })

    forecast["Condition"] = (
        forecast["WeatherCode"]
        .apply(get_weather_condition)
    )

    forecast["Activity"] = (
        forecast["Rainfall"]
        .apply(get_farming_activity)
    )

    forecast["Risk"] = (
        forecast["Rainfall"]
        .apply(get_weather_risk)
    )

    forecast["CardColor"] = (
        forecast["Rainfall"]
        .apply(get_card_color)
    )

    return {

        "current": current,

        "forecast": forecast

    }