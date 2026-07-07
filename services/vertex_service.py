import vertexai
from vertexai.generative_models import GenerativeModel

# ==========================================================
# Project Configuration
# ==========================================================

PROJECT_ID = "uzhu-ai-2026"
LOCATION = "us-central1"

# ==========================================================
# Initialize Vertex AI
# ==========================================================

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION
)

model = GenerativeModel("gemini-2.5-flash")

# ==========================================================
# AI Farming Advisor
# ==========================================================

def generate_farm_advice(
    state,
    district,
    crop,
    season,
    farm_size,
    budget,
    water,
    history,
    current_weather,
    forecast,
):

    prompt = f"""
You are UZHU AI,
an expert agriculture decision intelligence system.

Analyze the following farm.

Farmer Details

State: {state}

District: {district}

Crop: {crop}

Season: {season}

Farm Size: {farm_size} Acres

Budget: ₹{budget}

Water Availability: {water}

Historical Performance

Average Production:
{history["production"]:.2f}

Average Yield:
{history["yield"]:.2f}

Average Area:
{history["area"]:.2f}

Current Weather

Temperature:
{current_weather["temperature_2m"]} °C

Humidity:
{current_weather["relative_humidity_2m"]} %

Rainfall:
{current_weather["precipitation"]} mm

Wind Speed:
{current_weather["wind_speed_10m"]} km/h

7-Day Forecast

{forecast.to_string(index=False)}

Generate a professional farming report.

Return in Markdown.

Include exactly these sections:

## Summary

## Weather Analysis

## Irrigation Recommendation

## Fertilizer Recommendation

## Disease Risk

## Estimated Yield

## Estimated Profit

## Government Schemes

## Final Recommendation

Keep the response under 500 words.
"""

    response = model.generate_content(prompt)

    return response.text