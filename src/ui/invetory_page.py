import streamlit as st
import pandas as pd

def render_inventory_page(inventory_df):
    st.subheader("📦 Inventory Management")
    st.markdown("Update stock levels after receiving orders.")

    edited_df = st.data_editor(
        inventory_df,
        num_rows="fixed",
        use_container_width=True
    )
    return edited_df