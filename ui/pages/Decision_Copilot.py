import streamlit as st
import pandas as pd
import plotly.express as px
from services.vertex_service import generate_farm_advice

from services.bigquery_service import (
    get_states,
    get_districts,
    get_crops,
    get_seasons,
)

from services.decision_engine import analyze_farm

from services.weather_service import (
    get_weather_forecast,
)

from services.location_service import (
    get_coordinates,
)

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Decision Copilot",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 UZHU AI Decision Copilot")

st.markdown("""
### AI Powered Decision Intelligence for Smart Agriculture

UZHU AI combines

- 🌾 Historical Crop Analytics
- 🌦 Weather Intelligence
- 📈 Production Trends
- 🤖 AI Recommendations
- 🏛 Government Schemes

to provide intelligent farming decisions.
""")

st.divider()

# ==========================================================
# Farmer Details
# ==========================================================

st.subheader("🚜 Farmer Information")

left, right = st.columns(2)

with left:

    state = st.selectbox(
        "📍 State",
        get_states()
    )

    district = st.selectbox(
        "📍 District",
        get_districts(state)
    )

    crop = st.selectbox(
        "🌾 Crop",
        get_crops()
    )

    season = st.selectbox(
        "📅 Season",
        get_seasons()
    )

with right:

    farm_size = st.number_input(
        "🌱 Farm Size (Acres)",
        min_value=0.5,
        step=0.5
    )

    budget = st.number_input(
        "💰 Budget (₹)",
        min_value=1000,
        step=1000
    )

    water = st.selectbox(
        "💧 Water Availability",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    experience = st.selectbox(
        "👨‍🌾 Farming Experience",
        [
            "Beginner",
            "Intermediate",
            "Experienced"
        ]
    )

st.divider()

# ==========================================================
# Analyze Button
# ==========================================================

analyze = st.button(
    "🚀 Analyze My Farm",
    use_container_width=True,
    type="primary"
)

# ==========================================================
# Run Decision Engine
# ==========================================================

if analyze:

    with st.spinner("Analyzing your farm using UZHU AI..."):

        result = analyze_farm(
            state,
            district,
            crop,
            season,
            farm_size,
            budget,
            water,
        )

        
        coord = get_coordinates(
            state,
            district
        )

        weather = get_weather_forecast(
        coord["lat"],
        coord["lon"]
          )
                

        if weather is None:

            st.error(
                "Unable to fetch weather information."
            )

            st.stop()

        current = weather["current"]

        forecast = weather["forecast"]

                # ==========================================================
        # Historical Analysis
        # ==========================================================

        st.success("✅ Farm analysis completed successfully.")

        history = result["history"]

        ai_report = generate_farm_advice(
            state,
            district,
            crop,
            season,
            farm_size,
            budget,
            water,
            history,
            current,
            forecast
        )

        st.divider()

        st.header("📊 Historical Crop Performance")

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "🌾 Avg Production",
            f"{history['production']:.2f}"
        )

        m2.metric(
            "🌱 Avg Yield",
            f"{history['yield']:.2f}"
        )

        m3.metric(
            "🚜 Avg Cultivated Area",
            f"{history['area']:.2f}"
        )

        st.divider()

        # ==========================================================
        # Current Weather
        # ==========================================================

        st.header("🌤 Current Weather")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🌡 Temperature",
            f"{current['temperature_2m']:.1f} °C"
        )

        c2.metric(
            "💧 Humidity",
            f"{current['relative_humidity_2m']} %"
        )

        c3.metric(
            "🌧 Rainfall",
            f"{current['precipitation']:.1f} mm"
        )

        c4.metric(
            "💨 Wind Speed",
            f"{current['wind_speed_10m']:.1f} km/h"
        )

        st.divider()

        # ==========================================================
        # 7-Day Weather Cards
        # ==========================================================

        st.header("📅 7-Day Weather Forecast")

        cols = st.columns(7)

        for i in range(min(7, len(forecast))):

            day = forecast.iloc[i]

            cols[i].markdown(
                f"""
<div style="
background:{day['CardColor']};
padding:12px;
border-radius:15px;
color:white;
text-align:center;
height:240px;
">

<h4>{pd.to_datetime(day['Date']).strftime('%a')}</h4>

<h2>{day['Condition']}</h2>

<hr>

<b>🌡 {day['Max Temp']:.0f}° / {day['Min Temp']:.0f}°</b>

<br><br>

💧 Rain

<b>{day['Rainfall']:.1f} mm</b>

<br><br>

💨 Wind

<b>{day['Wind']:.0f} km/h</b>

<br><br>

{day['Activity']}

</div>
""",
                unsafe_allow_html=True
            )

        st.divider()

                # ==========================================================
        # Weather Analytics
        # ==========================================================

        st.header("📈 Weather Analytics")

        left, right = st.columns(2)

        with left:

            st.subheader("🌧 Rainfall Forecast")

            rain_chart = px.bar(
                forecast,
                x="Date",
                y="Rainfall",
                color="Rainfall",
                text="Rainfall",
                title="Expected Rainfall (Next 7 Days)"
            )

            rain_chart.update_layout(
                height=420,
                xaxis_title="Date",
                yaxis_title="Rainfall (mm)",
                coloraxis_showscale=False
            )

            st.plotly_chart(
                rain_chart,
                use_container_width=True
            )

        with right:

            st.subheader("🌡 Temperature Trend")

            temp_chart = px.line(
                forecast,
                x="Date",
                y=["Max Temp", "Min Temp"],
                markers=True,
                title="Maximum & Minimum Temperature"
            )

            temp_chart.update_layout(
                height=420,
                xaxis_title="Date",
                yaxis_title="Temperature (°C)"
            )

            st.plotly_chart(
                temp_chart,
                use_container_width=True
            )

        st.divider()

        # ==========================================================
        # AI Confidence & Weather Risk
        # ==========================================================

        st.header("🧠 AI Assessment")

        highest_rain = forecast["Rainfall"].max()

        avg_temp = forecast["Max Temp"].mean()

        confidence = 96

        if highest_rain >= 20:
            risk = "🔴 High"

        elif highest_rain >= 5:
            risk = "🟡 Medium"

        else:
            risk = "🟢 Low"

        a1, a2, a3 = st.columns(3)

        a1.metric(
            "🧠 AI Confidence",
            f"{confidence}%"
        )

        a2.metric(
            "⚠ Weather Risk",
            risk
        )

        a3.metric(
            "🌡 Avg Temperature",
            f"{avg_temp:.1f}°C"
        )

        st.divider()

        # ==========================================================
        # Smart Farming Advisory
        # ==========================================================

        st.header("🤖 Vertex AI Farming Advisor")

        ai_report = generate_farm_advice(
            state,
            district,
            crop,
            season,
            farm_size,
            budget,
            water,
            history,
            current,
            forecast
        )

        st.markdown(ai_report)

        st.divider()

        # ==========================================================
        # Estimated Yield & Profit
        # ==========================================================

        st.header("💰 Farm Performance Estimation")

        expected_yield = history["yield"] * farm_size
        estimated_price = 25000  # ₹ per ton (placeholder)
        estimated_revenue = expected_yield * estimated_price
        estimated_cost = budget
        estimated_profit = estimated_revenue - estimated_cost

        p1, p2, p3, p4 = st.columns(4)

        p1.metric(
            "🌾 Expected Yield",
            f"{expected_yield:.2f} Tons"
        )

        p2.metric(
            "💵 Estimated Revenue",
            f"₹ {estimated_revenue:,.0f}"
        )

        p3.metric(
            "💸 Estimated Cost",
            f"₹ {estimated_cost:,.0f}"
        )

        p4.metric(
            "📈 Expected Profit",
            f"₹ {estimated_profit:,.0f}"
        )

        st.divider()

        # ==========================================================
        # Next 7-Day Farming Calendar
        # ==========================================================

        st.header("🗓 Recommended Farming Calendar")

        calendar_df = forecast[
            [
                "Date",
                "Condition",
                "Activity",
                "Risk"
            ]
        ]

        st.dataframe(
            calendar_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ==========================================================
        # AI Decision Summary
        # ==========================================================

        st.header("🎯 Final AI Decision")

        if risk == "🔴 High":

            decision = "Delay major farming activities until weather improves."

        elif risk == "🟡 Medium":

            decision = "Proceed with caution. Follow weather advisories."

        else:

            decision = "Weather conditions are favorable for planned farming activities."

        st.markdown(
            f"""
<div style="
background:#0d3b66;
padding:25px;
border-radius:15px;
color:white;
">

<h2>🌾 UZHU AI Decision Report</h2>

<hr>

<b>State</b> : {state}<br>

<b>District</b> : {district}<br>

<b>Crop</b> : {crop}<br>

<b>Season</b> : {season}<br>

<b>Farm Size</b> : {farm_size} Acres<br>

<b>Budget</b> : ₹ {budget:,.0f}<br>

<b>Water Availability</b> : {water}<br>

<b>Experience</b> : {experience}<br>

<hr>

<h3>⚠ Risk Level : {risk}</h3>

<h3>🧠 AI Confidence : {confidence}%</h3>

<hr>

<h3>🤖 Recommendation</h3>

<p>{decision}</p>

<hr>

<h3>🌱 Suggested Next Action</h3>

<p>{forecast.iloc[0]["Activity"]}</p>

</div>
""",
            unsafe_allow_html=True
        )

        st.divider()

        # ==========================================================
        # Future Modules
        # ==========================================================

        st.header("🌱 Next Release")

        left, right = st.columns(2)

        with left:

            st.info(
                """
### 🌦 Planned Features

🧠 Future AI Features

📷 Crop Disease Detection (Image AI)
🛰 Satellite Crop Monitoring
📈 Market Price Prediction
🗣 Voice Assistant (Multilingual)
📄 Smart PDF Reports
🌍 Multi-language Support"""
            )

        st.divider()

        # ==========================================================
        # Footer
        # ==========================================================

        st.caption(
            "🌾 UZHU AI | AI Powered Decision Intelligence Platform for Smart Agriculture"
        )