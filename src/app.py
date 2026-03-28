import streamlit as st
import pandas as pd

from data import load_data, split_data, load_recipes, load_inventory
from features import build_features, compute_ingredient_demand, compute_order_quantity

from models import train_model, make_predictions, predict_next_day
from evaluation import evaluate_model

from src.ui import (
    render_header,
    render_sidebar,
    render_metrics,
    render_table,
    render_bar_chart,
    render_download,
    run_with_loading
)

def run_pipeline(df):

    # Feature engineering
    df_model = build_features(df)

    # Feature list
    features = [
        "day_of_week", "month", "week_of_year", "is_weekend",
        "lag_1", "lag_2", "lag_7", "lag_14",
        "rolling_avg_7", "rolling_avg_28"
    ]

    # Train/test split
    X_train, X_test, y_train, y_test, train, test = split_data(df_model, features)

    # Train model
    model = train_model(X_train, y_train)

    # Predict test set
    predictions = make_predictions(model, X_test)

    # Evaluate
    results = evaluate_model(y_test, predictions)

    # Next-day prediction
    next_day_predictions = predict_next_day(df_model, model, features)

    # Ingredient forecast
    recipes_df = load_recipes()
    ingredient_forecast = compute_ingredient_demand(
        next_day_predictions,
        recipes_df
    )

    # Order plan
    inventory_df = load_inventory()
    order_plan = compute_order_quantity(
        ingredient_forecast,
        inventory_df,
        safety_factor=0.1
    )

    return results, next_day_predictions, ingredient_forecast, order_plan


def main():

    # Header
    render_header()

    # Load data
    df = load_data()

    # Sidebar
    selected_store, run_button = render_sidebar(df)

    if not run_button:
        return

 
    def pipeline():
        return run_pipeline(df)

    results, next_day_predictions, ingredient_forecast, order_plan = run_with_loading(pipeline)

    next_day_predictions = next_day_predictions[
        next_day_predictions["store_id"] == selected_store
    ]

    ingredient_forecast = ingredient_forecast[
        ingredient_forecast["store_id"] == selected_store
    ]

    order_plan = order_plan[
        order_plan["store_id"] == selected_store
    ]

    # Metrics
    render_metrics(results)

    # Item Forecast
    render_table("📅 Next-Day Item Forecast", next_day_predictions)

    # Ingredient Forecast
    render_table("🥩 Ingredient Forecast", ingredient_forecast)

    render_bar_chart(
        ingredient_forecast,
        x_col="ingredient_id",
        y_col="ingredient_quantity",
        title="Ingredient Demand"
    )

    # Order Plan
    render_table("🛒 Order Plan", order_plan)

    render_bar_chart(
        order_plan,
        x_col="ingredient_id",
        y_col="order_quantity",
        title="Order Quantities"
    )

    # Download button
    render_download(order_plan, "order_plan.csv")

if __name__ == "__main__":
    main()