import streamlit as st

from data import load_data, split_data
from evaluation import evaluate_model
from features import build_features
from models import make_predictions, predict_next_day, train_model
from ui import (
    render_header,
    render_sidebar,
    run_with_loading,
    show_forecast_tab,
    show_inventory_tab,
)


def run_pipeline(df):
    df_model = build_features(df)
    features = [
        "day_of_week", "month", "week_of_year", "is_weekend",
        "lag_1", "lag_2", "lag_7", "lag_14",
        "rolling_avg_7", "rolling_avg_28",
    ]

    X_train, X_test, y_train, y_test, _, _ = split_data(df_model, features)
    model = train_model(X_train, y_train)
    results = evaluate_model(y_test, make_predictions(model, X_test))
    return results, predict_next_day(df_model, model, features)


def main():

    render_header()
    df = load_data()
    selected_store, run_button = render_sidebar(df)

    if run_button:
        results, next_day_predictions = run_with_loading(lambda: run_pipeline(df))
        st.session_state["results"] = results
        st.session_state["predictions"] = next_day_predictions

    if "results" not in st.session_state:
        return

    tab_choice = st.radio(
        "Select view",
        ["Forecast", "Inventory"],
        index=0 if st.session_state.get("active_tab") != "Inventory" else 1,
        horizontal=True,
    )
    st.session_state["active_tab"] = tab_choice

    if tab_choice == "Forecast":
        show_forecast_tab(
            st.session_state["predictions"],
            selected_store,
            st.session_state["results"],
        )
    else:
        show_inventory_tab()


if __name__ == "__main__":
    main()
