import streamlit as st

from data import load_data, split_data, load_recipes, load_inventory, save_inventory
from features import build_features, compute_ingredient_demand, compute_order_quantity
from models import train_model, make_predictions, predict_next_7_days, predict_next_day
from evaluation import evaluate_model
from login import check_login

from ui import (
    render_header,
    render_sidebar,
    render_metrics,
    render_table,
    render_bar_chart,
    render_download,
    run_with_loading,
    render_inventory_page,
    show_forecast_tab,
    show_inventory_tab
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

   

    next_day_predictions = predict_next_day(df_model, model, features)

    return results, next_day_predictions


def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if check_login(username, password):
                st.session_state["logged_in"] = True
                st.success("Login successful!")
                return
            else:
                st.error("Invalid username or password.")
        return

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

    if "active_tab" not in st.session_state:
        st.session_state["active_tab"] = "📊 Forecast"

    tab_choice = st.radio(
        "Select View:",
        ["📊 Forecast", "📦 Inventory"],
        index=["📊 Forecast", "📦 Inventory"].index(st.session_state["active_tab"]),
        horizontal=True
    )
    st.session_state["active_tab"] = tab_choice

    if tab_choice == "📊 Forecast":
        show_forecast_tab(next_day_predictions, selected_store, results)
    
    elif tab_choice == "📦 Inventory":
        show_inventory_tab()

if __name__ == "__main__":
    main()