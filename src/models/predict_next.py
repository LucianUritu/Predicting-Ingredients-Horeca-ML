import pandas as pd

def predict_next_day(df, model, features):
    """
    Predict next day for all store-item combinations,
    using only data up to the current day.
    """

    df = df.copy()
    df["sales_date"] = pd.to_datetime(df["sales_date"])

    # Current day (t)
    current_day = pd.Timestamp.today().normalize()

    # Keep only history up to current day
    df = df[df["sales_date"] <= current_day].copy()

    # Predict next day (t + 1)
    next_date = pd.Timestamp.today().normalize()

    predictions = []
    group_cols = ["store_id", "menu_item_id"]

    for (store, item), group in df.groupby(group_cols):
        group = group.sort_values("sales_date")

        # Take last rows needed for lag features
        last_28_days = group.tail(28)
        lags = last_28_days["quantity_sold"].tolist()

        # Skip if not enough history
        if len(lags) < 14:
            continue

        row = {
            "store_id": store,
            "menu_item_id": item,
            "sales_date": next_date,

            # Calendar features
            "day_of_week": next_date.weekday(),
            "month": next_date.month,
            "week_of_year": int(next_date.isocalendar().week),
            "is_weekend": 1 if next_date.weekday() >= 5 else 0,

            # Lag features
            "lag_1": lags[-1],
            "lag_2": lags[-2],
            "lag_7": lags[-7],
            "lag_14": lags[-14],

            # Rolling features
            "rolling_avg_7": last_28_days["quantity_sold"].tail(7).mean(),
            "rolling_avg_28": last_28_days["quantity_sold"].mean(),
        }

        predictions.append(row)

    pred_df = pd.DataFrame(predictions)

    if pred_df.empty:
        raise ValueError("No predictions could be generated. Not enough history up to the current day.")

    X_pred = pred_df[features]
    pred_df["predicted_quantity"] = model.predict(X_pred)

    return pred_df