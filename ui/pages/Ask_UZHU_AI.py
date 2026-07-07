import streamlit as st

from services.ask_ai_service import ask_uzhu_ai
from services.bigquery_service import (
    get_states,
    get_districts,
    get_crops,
)

from services.location_service import get_coordinates

from services.weather_service import get_weather_forecast

from services.decision_engine import analyze_farm

# ==========================================================
# Page
# ==========================================================

st.title("💬 Ask UZHU AI")

st.markdown("""
### Your AI Agriculture Assistant

Ask questions about

🌾 Crops

🌦 Weather

🦠 Diseases

🐛 Pests

💧 Irrigation

🧪 Fertilizers

🏛 Government Schemes

📈 Market Prices

🤖 Smart Farming
""")

st.divider()

# ==========================================================
# Session State
# ==========================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================================
# Farmer Context
# ==========================================================

st.subheader("🌾 Farm Context")

left, right = st.columns(2)

with left:

    state = st.selectbox(
        "State",
        get_states(),
        key="chat_state"
    )

    district = st.selectbox(
        "District",
        get_districts(state),
        key="chat_district"
    )

with right:

    crop = st.selectbox(
        "Crop",
        get_crops(),
        key="chat_crop"
    )

st.divider()

# ==========================================================
# Suggested Questions
# ==========================================================

st.subheader("💡 Suggested Questions")

examples = [
    "Which crop is best this season?",
    "Can I irrigate tomorrow?",
    "Will rain affect my crop?",
    "How can I increase my yield?",
    "Which fertilizer should I use?",
    "Which government schemes can I apply for?",
    "How do I prevent pest attacks?",
    "What disease risk is expected this week?"
]

cols = st.columns(2)

for i, question in enumerate(examples):

    if cols[i % 2].button(
        question,
        use_container_width=True
    ):
        st.session_state.example_question = question

st.divider()

# ==========================================================
# Question Input
# ==========================================================

default_question = st.session_state.get(
    "example_question",
    ""
)

question = st.text_area(
    "Ask your farming question",
    value=default_question,
    height=120,
    placeholder="Example: Can I irrigate my rice crop tomorrow?"
)

# ==========================================================
# Ask Button
# ==========================================================

col1, col2 = st.columns([3,1])

with col1:

    ask = st.button(
        "🤖 Ask UZHU AI",
        use_container_width=True,
        type="primary"
    )

with col2:

    clear = st.button(
        "🗑 Clear Chat",
        use_container_width=True
    )

if clear:

    st.session_state.chat_history = []

    st.rerun()

# ==========================================================
# Generate Response
# ==========================================================

if ask:

    if question.strip() == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner("UZHU AI is thinking..."):

            coord = get_coordinates(
                state,
                district
            )

            weather_data = get_weather_forecast(
                coord["lat"],
                coord["lon"]
            )

            history_result = analyze_farm(
                state,
                district,
                crop,
                "",
                1,
                1000,
                "Medium",
            )

            history = None

            if history_result["status"] == "success":

                history = history_result["history"]

            answer = ask_uzhu_ai(
            question=question,
            state=state,
            district=district,
            crop=crop,
            weather=weather_data["current"],
            history=history,
            forecast=weather_data["forecast"],
            chat_history=st.session_state.chat_history
        )

            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": answer
                }
            )

        if len(st.session_state.chat_history) > 10:

            st.session_state.chat_history = (
                st.session_state.chat_history[-10:]
            )

# ==========================================================
# Chat History
# ==========================================================

if st.session_state.chat_history:

    st.divider()

    st.header("💬 Conversation")

    for chat in reversed(st.session_state.chat_history):

        with st.chat_message("user"):

            st.markdown(chat["question"])

        with st.chat_message("assistant"):

            st.markdown(chat["answer"])

st.divider()

# ==========================================================
# Footer
# ==========================================================

st.caption(
    "🌾 UZHU AI | AI Powered Agriculture Assistant"
)