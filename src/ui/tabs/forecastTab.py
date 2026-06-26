import streamlit as st

from data import load_inventory, load_recipes
from features import compute_ingredient_demand, compute_order_quantity

from .. import (
    render_bar_chart,
    render_download,
    render_metrics,
    render_table,
)


def show_forecast_tab(next_day_predictions, selected_store, results):
    available_dates = sorted(next_day_predictions["sales_date"].unique())
    selected_date = st.selectbox("Select forecast day", available_dates)
    filtered_predictions = next_day_predictions[
        (next_day_predictions["sales_date"] == selected_date)
        & (next_day_predictions["store_id"] == selected_store)
    ]

    render_metrics(results)
    render_table("Item forecast", filtered_predictions)

    try:
        recipes_df = load_recipes()
    except FileNotFoundError:
        st.info(
            "Ingredient and order forecasts are unavailable until a recipes.csv "
            "file is provided. Item forecasts are still ready to use."
        )
        return

    ingredient_forecast = compute_ingredient_demand(
        filtered_predictions,
        recipes_df,
    )
    if ingredient_forecast.empty:
        st.warning(
            "None of the forecast products has a matching recipe. Add recipes "
            "using the same canonical menu-item names to calculate ingredients."
        )
        return

    render_table("Ingredient forecast", ingredient_forecast)
    render_bar_chart(
        ingredient_forecast,
        x_col="ingredient_id",
        y_col="ingredient_quantity",
        title="Ingredient demand",
    )

    try:
        inventory_df = load_inventory()
    except FileNotFoundError:
        st.info(
            "Ingredient demand is available. Add inventory.csv to calculate an "
            "order plan."
        )
        return

    order_plan = compute_order_quantity(
        ingredient_forecast,
        inventory_df,
        safety_factor=0.1,
    )
    render_table("Order plan", order_plan)
    render_bar_chart(
        order_plan,
        x_col="ingredient_id",
        y_col="order_quantity",
        title="Order quantities",
    )
    render_download(order_plan, "order_plan.csv")
