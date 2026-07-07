from vertexai.generative_models import GenerativeModel
import vertexai

# ==========================================================
# Vertex AI Configuration
# ==========================================================

PROJECT_ID = "uzhu-ai-2026"
LOCATION = "us-central1"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION
)

model = GenerativeModel("gemini-2.5-flash")

# ==========================================================
# Ask UZHU AI
# ==========================================================

def ask_uzhu_ai(
    question,
    state="",
    district="",
    crop="",
    weather=None,
    history=None,
    forecast=None,
    chat_history=None,
):

    history_text = "No historical data available."

    if history:

        history_text = f"""
Historical Crop Data

Average Production : {history.get("production","N/A")}
Average Yield : {history.get("yield","N/A")}
Average Area : {history.get("area","N/A")}
"""

    weather_text = "Weather information unavailable."

    if weather:

        weather_text = f"""
Current Weather

Temperature : {weather.get("temperature_2m")} °C
Humidity : {weather.get("relative_humidity_2m")} %
Rainfall : {weather.get("precipitation")} mm
Wind Speed : {weather.get("wind_speed_10m")} km/h
"""

    forecast_text = ""

    if forecast is not None:

        forecast_text = forecast.to_string(index=False)

    conversation = ""

    if chat_history:

        for chat in chat_history[-5:]:

            conversation += f"""
User: {chat['question']}

Assistant: {chat['answer']}

"""

    prompt = f"""
You are UZHU AI.

You are an expert AI Agriculture Assistant.

===================================

Farmer Context

State: {state}

District: {district}

Crop: {crop}

===================================

{history_text}

===================================

{weather_text}

===================================

7-Day Forecast

{forecast_text}

===================================

Previous Conversation

{conversation}

===================================

Current Question

{question}

===================================

Instructions

• Answer in simple English.
• Use weather information whenever relevant.
• Use historical crop data whenever relevant.
• Remember previous conversation.
• Give practical farming advice.
• Mention risks.
• Mention government schemes if relevant.
• Never invent facts.
• End with Recommended Next Step.

Maximum 400 words.
"""

    response = model.generate_content(prompt)

    return response.text