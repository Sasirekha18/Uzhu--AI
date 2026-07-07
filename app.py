import streamlit as st

st.set_page_config(
    page_title="UZHU AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

dashboard = st.Page(
    "ui/pages/Dashboard.py",
    title="Dashboard",
    icon="🏠"
)

analytics = st.Page(
    "ui/pages/Analytics.py",
    title="Analytics",
    icon="📊"
)

copilot = st.Page(
    "ui/pages/Decision_Copilot.py",
    title="Decision Copilot",
    icon="🧠"
)

ask_ai = st.Page(
    "ui/pages/Ask_UZHU_AI.py",
    title="Ask UZHU AI",
    icon="💬"
)

schemes = st.Page(
    "ui/pages/Government_Schemes.py",
    title="Government Schemes",
    icon="🏛️"
)

impact = st.Page(
    "ui/pages/Impact.py",
    title="Community Impact",
    icon="🌍"
)

pg = st.navigation([
    dashboard,
    analytics,
    copilot,
    ask_ai,
    schemes,
    impact
])

pg.run()