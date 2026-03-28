import streamlit as st

def render_download(df, filename):
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label = "📥 Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )