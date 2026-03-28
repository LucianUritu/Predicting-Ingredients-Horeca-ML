import streamlit as st

def render_header():
    st.set_page_config(page_title="Horeca AI", layout="wide")
    st.title("Horeca AI Forecasting System")

    st.markdown("""
    This system predicts:
    - 📊 Item demand
    - 🥩 Ingredient needs
    - 🛒 What to order tomorrow
    """)

    