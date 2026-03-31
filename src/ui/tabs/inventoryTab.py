import streamlit as st

from data import load_inventory, save_inventory

from src.ui import (
    render_inventory_page,
)

def show_inventory_tab():
    inventory_df = load_inventory()
    updated_inventory = render_inventory_page(inventory_df)
    if st.button("💾 Save Inventory Changes"):
        save_inventory(updated_inventory)
        st.success("Inventory updated successfully!")
        st.session_state["active_tab"] = "📦 Inventory"
    return st.session_state