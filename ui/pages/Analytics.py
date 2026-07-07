import streamlit as st
import plotly.express as px

from services.bigquery_service import (
    get_crop_data,
    get_states,
    get_districts,
    get_crops,
    get_seasons,
    get_years,
)

st.title("📊 Analytics Dashboard")

df = get_crop_data()

st.divider()

col1,col2,col3 = st.columns(3)

with col1:
    state = st.selectbox(
        "State",
        ["All"] + get_states()
    )

with col2:
    crop = st.selectbox(
        "Crop",
        ["All"] + get_crops()
    )

with col3:
    season = st.selectbox(
        "Season",
        ["All"] + get_seasons()
    )

if state != "All":
    df = df[df["State"] == state]

if crop != "All":
    df = df[df["Crop"] == crop]

if season != "All":
    df = df[df["Season"] == season]

st.divider()

st.subheader("📈 Production by Crop")

production = (
    df.groupby("Crop")["Production"]
    .sum()
    .reset_index()
)

fig = px.bar(
    production,
    x="Crop",
    y="Production"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("🗺 State Production")

state_df = (
    df.groupby("State")["Production"]
    .sum()
    .reset_index()
)

fig = px.bar(
    state_df,
    x="State",
    y="Production"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("📅 Year Wise Production")

year_df = (
    df.groupby("Crop_Year")["Production"]
    .sum()
    .reset_index()
)

fig = px.line(
    year_df,
    x="Crop_Year",
    y="Production",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("🌾 Yield vs Area")

fig = px.scatter(
    df,
    x="Area",
    y="Yield",
    color="Crop"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("🤖 AI Insight")

highest = production.sort_values(
    "Production",
    ascending=False
).iloc[0]

st.success(
    f"""
Highest producing crop is **{highest['Crop']}**

Total Production:

**{highest['Production']:,.0f}**

UZHU AI recommends this crop based on historical production trends.
"""
)