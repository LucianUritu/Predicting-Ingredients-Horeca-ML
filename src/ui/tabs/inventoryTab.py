import streamlit as st

from data import load_inventory, save_inventory

from .. import render_inventory_page


def show_inventory_tab():
    try:
        inventory_df = load_inventory()
    except FileNotFoundError:
        st.info("Inventory management will be available once inventory.csv is provided.")
        return st.session_state

    updated_inventory = render_inventory_page(inventory_df)
    if st.button("Save inventory changes"):
        save_inventory(updated_inventory)
        st.success("Inventory updated successfully.")
        st.session_state["active_tab"] = "Inventory"
    return st.session_state
