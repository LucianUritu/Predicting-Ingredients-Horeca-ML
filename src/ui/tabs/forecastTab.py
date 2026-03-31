import streamlit as st

from data import load_recipes, load_inventory
from features import compute_ingredient_demand, compute_order_quantity

from .. import (
    render_metrics,
    render_table,
    render_bar_chart,
    render_download
)

def show_forecast_tab(next_day_predictions, selected_store, results):
    available_dates = sorted(next_day_predictions["sales_date"].unique())
    selected_date = st.selectbox(
            "📅 Select Forecast Day",
            available_dates
        )
    filtered_predictions = next_day_predictions[
            (next_day_predictions["sales_date"] == selected_date) &
            (next_day_predictions["store_id"] == selected_store)
        ]
    recipes_df = load_recipes()
    ingredient_forecast = compute_ingredient_demand(
            filtered_predictions,
            recipes_df
        )
    inventory_df = load_inventory()
    order_plan = compute_order_quantity(
            ingredient_forecast,
            inventory_df,
            safety_factor=0.1
        )
    render_metrics(results)
    render_table("📅 Item Forecast", filtered_predictions)
    render_table("🥩 Ingredient Forecast", ingredient_forecast)
    render_bar_chart(
            ingredient_forecast,
            x_col="ingredient_id",
            y_col="ingredient_quantity",
            title="Ingredient Demand"
        )
    render_table("🛒 Order Plan", order_plan)
    render_bar_chart(
            order_plan,
            x_col="ingredient_id",
            y_col="order_quantity",
            title="Order Quantities"
        )
    render_download(order_plan, "order_plan.csv")