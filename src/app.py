import streamlit as st
import pandas as pd

from data import load_data, split_data, load_recipes, load_inventory
from features import build_features, compute_ingredient_demand, compute_order_quantity

from models import train_model, make_predictions, predict_next_day
from evaluation import evaluate_model

st.set_page_config(page_title="Horeca AI", layout="wide")
st.title("Horeca AI Forecasting System")

st.markdown("""
This system predicts:
- 📊 Item demand
- 🥩 Ingredient needs
- 🛒 What to order tomorrow
""")

if st.button("Run Forecast Pipeline"):

    st.info("Running pipeline...")

    df = load_data()
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

    st.success("✅ Model trained successfully!")


    # Model Performance:
    st.subheader("📊 Model Performance")

    col1, col2 = st.columns(2)
    col1.metric("MAE",  results["MAE"])
    col2.metric("RMSE", results["RMSE"])

    # Next Day Performance:
    st.subheader("📅 Next-Day Item Forecast")
    next_day_predictions = predict_next_day(df_model, model, features)
    st.dataframe(next_day_predictions)

    st.subheader("🥩 Ingredient Forecast")

    recipes_df = load_recipes()
    ingredient_forecast = compute_ingredient_demand(
        next_day_predictions,
        recipes_df
    )
    st.dataframe(ingredient_forecast)

    st.subheader("🛒 Order Recommendations")
    inventory_df = load_inventory()

    order_plan = compute_order_quantity(
        ingredient_forecast,
        inventory_df,
        safety_factor=0.1
    )

    st.dataframe(order_plan)
    st.success("🎯 Forecast completed!")

    st.markdown("---")
    st.markdown("Built with ❤️ for Horeca optimization")    