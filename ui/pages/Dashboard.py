import streamlit as st

from ui.components.banner import show_banner
from ui.components.metrics import show_metrics

from services.bigquery_service import (
    get_dashboard_stats,
    get_crop_data,
    get_states,
    get_crop_data_filtered,
)

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="UZHU AI",
    page_icon="🌾",
    layout="wide"
)

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

stats = get_dashboard_stats()
crop_data = get_crop_data()

# ----------------------------------------------------
# Banner
# ----------------------------------------------------

show_banner()

st.divider()

# ----------------------------------------------------
# Mission
# ----------------------------------------------------

st.header("🎯 Mission")

st.markdown("""
UZHU AI empowers farmers through **AI-powered Decision Intelligence**.

The platform combines:

- 🌦 Weather Intelligence
- 🌱 Crop Analytics
- 🤖 AI Recommendations
- 📈 Market Insights
- 🏛 Government Schemes

to help farmers make smarter, data-driven agricultural decisions.
""")

st.divider()

# ----------------------------------------------------
# Dashboard Metrics
# ----------------------------------------------------

show_metrics(stats)

st.divider()

# ----------------------------------------------------
# Crop Explorer
# ----------------------------------------------------

st.header("🌱 Crop Explorer")

col1, col2 = st.columns(2)

with col1:
    selected_crop = st.selectbox(
        "Select Crop",
        sorted(crop_data["Crop"].unique())
    )

with col2:
    selected_state = st.selectbox(
        "Select State",
        get_states()
    )

filtered = crop_data[
    (crop_data["Crop"] == selected_crop) &
    (crop_data["State"] == selected_state)
]

st.dataframe(
    filtered,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# Production Trend
# ----------------------------------------------------

st.header("📈 Top Crop Production")

chart_df = (
    crop_data
    .groupby("Crop", as_index=False)["Production"]
    .sum()
    .sort_values("Production", ascending=False)
    .head(10)
)

st.bar_chart(
    chart_df.set_index("Crop")
)

st.divider()

# ----------------------------------------------------
# Top Producing States
# ----------------------------------------------------

st.header("🗺️ Top Producing States")

state_df = (
    crop_data
    .groupby("State", as_index=False)["Production"]
    .sum()
    .sort_values("Production", ascending=False)
    .head(10)
)

st.bar_chart(
    state_df.set_index("State")
)

st.divider()

# ----------------------------------------------------
# AI Summary
# ----------------------------------------------------

st.header("🤖 AI Crop Insights")

highest_crop = chart_df.iloc[0]["Crop"]

highest_prod = chart_df.iloc[0]["Production"]

st.success(f"""
### AI Summary

✅ Highest Producing Crop : **{highest_crop}**

📈 Estimated Production : **{highest_prod:,.0f}**

💡 UZHU AI will soon provide:

- AI Crop Recommendation
- Weather Intelligence
- Disease Prediction
- Fertilizer Recommendation
- Government Scheme Recommendation
- Profitability Analysis
""")

st.divider()

# ----------------------------------------------------
# Top Producing Crops
# ----------------------------------------------------

st.header("🏆 Top Producing Crops")

st.dataframe(
    chart_df,
    use_container_width=True
)

st.divider()



# ----------------------------------------------------
# Footer
# ----------------------------------------------------

st.caption(
    "🌾 UZHU AI | AI Powered Decision Intelligence Platform for Smart Agriculture"
)