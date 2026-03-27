import pandas as pd

def predict_next_day(df, model, features):
    """
        Predict next day for All store-item combinations
    """

    # Get last available data (t)
    last_date = df["sales_date"].max()

    # Create next day (t + 1)
    next_date = last_date + pd.Timedelta(days=1)

    predictions = []

    group_cols = ["store_id", "menu_item_id"]

    for (store, item), group in df.groupby(group_cols):
        group = group.sort_values("sales_date")
        
        # Take last rows needed for lag
        last_28_days = group.tail(28)


        row = {}
        row["store_id"]     = store
        row["menu_item_id"] = item
        row["sales_date"]   = next_date

        # Calendar Features
        row["day_of_week"] = next_date.weekday()
        row["month"] = next_date.month
        row["week_of_year"] = next_date.isocalendar().week
        row["is_weekend"] = 1 if next_date.weekday() >= 5 else 0

        lags = last_28_days["quantity_sold"].tolist()
        row["lag_1"] = lags[-1] if len(lags) >= 1 else None
        row["lag_2"] = lags[-2] if len(lags) >= 2 else None
        row["lag_7"] = lags[-7] if len(lags) >= 7 else None
        row["lag_14"] = lags[-14] if len(lags) >= 14 else None

        # Rolling features
        row["rolling_avg_7"] = last_28_days["quantity_sold"].tail(7).mean() if len(lags) >= 7 else None
        row["rolling_avg_28"] = last_28_days["quantity_sold"].mean() if len(lags) >= 1 else None

        predictions.append(row)

    # Convert to DataFrame
    pred_df = pd.DataFrame(predictions)

    # Keep only features
    X_pred = pred_df[features]

    # Predict
    pred_df["predicted_quantity"] = model.predict(X_pred)

    return pred_df