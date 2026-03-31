import streamlit as st

def render_sidebar(df):
    st.sidebar.header("⚙️ Controls")

    stores = df["store_id"].unique()
    selected_store = st.sidebar.selectbox("Select Store", stores)

    run_button = st.sidebar.button("🚀 Run Forecast")

    return selected_store, run_button

