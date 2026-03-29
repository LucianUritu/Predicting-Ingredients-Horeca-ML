import streamlit as st

from data import load_data, split_data, load_recipes, load_inventory, save_inventory
from features import build_features, compute_ingredient_demand, compute_order_quantity
from models import train_model, make_predictions, predict_next_7_days
from evaluation import evaluate_model

from src.ui import (
    render_header,
    render_sidebar,
    render_metrics,
    render_table,
    render_bar_chart,
    render_download,
    run_with_loading,
    render_inventory_page
)

def run_pipeline(df):

    df_model = build_features(df)

    features = [
        "day_of_week", "month", "week_of_year", "is_weekend",
        "lag_1", "lag_2", "lag_7", "lag_14",
        "rolling_avg_7", "rolling_avg_28"
    ]

    X_train, X_test, y_train, y_test, train, test = split_data(df_model, features)

    model = train_model(X_train, y_train)

    predictions = make_predictions(model, X_test)

    results = evaluate_model(y_test, predictions)

   
    next_day_predictions = predict_next_7_days(df_model, model, features, days=7)

    return results, next_day_predictions


def main():

    render_header()

    df = load_data()

    selected_store, run_button = render_sidebar(df)

    if run_button:

        def pipeline():
            return run_pipeline(df)

        results, next_day_predictions = run_with_loading(pipeline)

        st.session_state["results"] = results
        st.session_state["predictions"] = next_day_predictions

    if "results" not in st.session_state:
        return

    results = st.session_state["results"]
    next_day_predictions = st.session_state["predictions"]

    tab1, tab2 = st.tabs(["📊 Forecast", "📦 Inventory"])

    # FORECAST TAB:
    with tab1:
        
            
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

    with tab2:
        invetory_df = load_inventory()
        updated_inventory = render_inventory_page(inventory_df)
        if st.button("💾 Save Inventory Changes"):
            save_inventory(updated_inventory)
            st.success("Inventory updated successfully!")

if __name__ == "__main__":
    main()