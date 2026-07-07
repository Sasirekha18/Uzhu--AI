import streamlit as st


def show_metrics(stats):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("States", stats["states"])

    with col2:
        st.metric("Districts", stats["districts"])

    with col3:
        st.metric("Crops", stats["crops"])

    with col4:
        st.metric("Records", f"{stats['records']:,}")