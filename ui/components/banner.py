import streamlit as st


def show_banner():
    st.markdown(
        """
        <div style='text-align:center;padding:15px;'>
            <h1>🌾 UZHU AI</h1>
            <h3>AI Powered Decision Intelligence Platform for Smart Agriculture</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.success("Welcome to UZHU AI")