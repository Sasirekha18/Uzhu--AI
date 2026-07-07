import streamlit as st
import pandas as pd

from services.bigquery_service import (
    get_states,
    get_crops,
)

from data.government_schemes import schemes

st.title("🏛 Government Schemes")

st.markdown("""
### Find Government Schemes suitable for your farm
""")

st.divider()

# ---------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    state = st.selectbox(
        "State",
        get_states()
    )

with col2:

    crop = st.selectbox(
        "Crop",
        get_crops()
    )

st.divider()

df = pd.DataFrame(schemes)

filtered = df[
    (
        (df["state"]=="All")
        |
        (df["state"]==state)
    )
    &
    (
        (df["crop"]=="All")
        |
        (df["crop"]==crop)
    )
]

st.metric(
    "Matching Schemes",
    len(filtered)
)

st.divider()

for _,row in filtered.iterrows():

    st.markdown(f"""
<div style="
background:#F5F7FA;
padding:20px;
border-radius:15px;
margin-bottom:20px;
border-left:6px solid #2E7D32;
">

<h3>🏛 {row['name']}</h3>

<b>Applicable Crop:</b> {row['crop']}<br>

<b>Benefit:</b> {row['benefit']}<br>

<b>Eligibility:</b> {row['eligibility']}<br>

<a href="{row['link']}" target="_blank">
Official Website
</a>

</div>
""",
unsafe_allow_html=True
)

st.divider()

st.info("""
🤖 Soon this page will use Vertex AI to recommend the best schemes
based on your crop, location, weather and farm details.
""")

st.caption(
"🌾 UZHU AI | Government Scheme Intelligence"
)