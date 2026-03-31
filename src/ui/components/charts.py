import streamlit as st

def render_bar_chart(df, x_col, y_col, title):
    st.subheader(title)
    st.bar_chart(df.set_index(x_col)[y_col])