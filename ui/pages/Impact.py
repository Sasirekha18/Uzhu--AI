import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Community Impact",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Community Impact")

st.markdown("""
### Measuring the real-world impact of UZHU AI on sustainable agriculture.
""")

st.divider()

# ==========================================================
# KPI Cards
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "👨‍🌾 Farmers Assisted",
    "1,250",
    "+142"
)

c2.metric(
    "💧 Water Saved",
    "2.8 M Litres",
    "+11%"
)

c3.metric(
    "🌾 Yield Improvement",
    "18%",
    "+4%"
)

c4.metric(
    "🤖 AI Recommendations",
    "9,850",
    "+1,204"
)

st.divider()

# ==========================================================
# SDG Goals
# ==========================================================

st.header("🎯 Sustainable Development Goals")

col1, col2 = st.columns(2)

with col1:

    st.success("""
### SDG 2 — Zero Hunger

• Improve crop productivity

• Better farming decisions

• Increased food security
""")

    st.success("""
### SDG 6 — Clean Water

• Smart irrigation

• Water conservation

• Efficient resource usage
""")

with col2:

    st.success("""
### SDG 12 — Responsible Consumption

• Reduce fertilizer waste

• Sustainable farming

• Optimize farm resources
""")

    st.success("""
### SDG 13 — Climate Action

• Weather intelligence

• Climate-aware farming

• Reduce environmental impact
""")

st.divider()

# ==========================================================
# Charts
# ==========================================================

st.header("📊 Community Analytics")

farmers = pd.DataFrame({

    "State":[
        "Tamil Nadu",
        "Karnataka",
        "Kerala",
        "Maharashtra",
        "Andhra Pradesh"
    ],

    "Farmers":[
        320,
        280,
        160,
        260,
        230
    ]

})

water = pd.DataFrame({

    "Crop":[
        "Rice",
        "Cotton",
        "Sugarcane",
        "Maize",
        "Groundnut"
    ],

    "Water Saved":[
        850000,
        420000,
        380000,
        290000,
        220000
    ]

})

left, right = st.columns(2)

with left:

    fig = px.bar(
        farmers,
        x="State",
        y="Farmers",
        color="Farmers",
        title="Farmers Supported by State"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.bar(
        water,
        x="Crop",
        y="Water Saved",
        color="Water Saved",
        title="Estimated Water Saved"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================================
# AI Adoption
# ==========================================================

st.header("🤖 AI Adoption")

adoption = pd.DataFrame({

    "Month":[
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun"
    ],

    "Recommendations":[
        1200,
        1800,
        2600,
        4200,
        6500,
        9850
    ]

})

fig = px.line(

    adoption,

    x="Month",

    y="Recommendations",

    markers=True,

    title="AI Recommendations Generated"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# Success Stories
# ==========================================================

st.header("🌾 Farmer Success Stories")

left, right = st.columns(2)

with left:

    st.info("""
### 👨‍🌾 Farmer - Tamil Nadu

Crop : Rice

✅ Reduced irrigation by 20%

✅ Increased yield by 15%

✅ Received PM-KISAN support

✅ Used AI weather recommendations
""")

with right:

    st.info("""
### 👩‍🌾 Farmer - Karnataka

Crop : Maize

✅ Improved fertilizer usage

✅ Water savings of 18%

✅ Better crop planning

✅ Reduced disease risk
""")

st.divider()

# ==========================================================
# Environmental Impact
# ==========================================================

st.header("🌱 Environmental Impact")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "💧 Water Conserved",
    "2.8 M L"
)

m2.metric(
    "🌾 Extra Food Production",
    "850 Tons"
)

m3.metric(
    "🌍 CO₂ Reduction",
    "12 Tons"
)

m4.metric(
    "🧪 Fertilizer Optimized",
    "18%"
)

st.divider()

# ==========================================================
# Future Vision
# ==========================================================

st.header("🚀 Future Vision")

st.success("""
UZHU AI aims to build a nationwide AI-powered agricultural ecosystem where:

• Every farmer receives personalized AI guidance.

• Water resources are conserved efficiently.

• Crop productivity improves sustainably.

• Government schemes reach eligible farmers.

• Communities become resilient to climate change.

• AI empowers every farming decision.
""")

st.caption(
    "🌾 UZHU AI | AI Powered Decision Intelligence Platform for Smart Agriculture"
)