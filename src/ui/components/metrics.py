import streamlit as st

def render_metrics(results):
    st.subheader("📊 Model Performance")

    col1, col2 = st.columns(2)
    col1.metric("MAE",  results["MAE"])
    col2.metric("RMSE", results["RMSE"])