import streamlit as st

def render_table(title, df):
    st.subheader(title)
    st.dataframe(df, use_container_width=True)