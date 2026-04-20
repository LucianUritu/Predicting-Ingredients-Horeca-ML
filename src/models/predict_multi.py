import pandas as pd

def predict_next_7_days(df, model, features, days=7):

    df = df.copy()
    results = []

    group_cols = ["store_id", "menu_item_id"]
    last_date = df["sales_date"].max()

    for day in range(1, days + 1):
        next_date = last_date + pd.Timedelta(days = day)
        predictions = []

        for (store, item), group in df.groupby(group_cols):
            group = group.sort_values("sales_date")

            last_28_days = group.tail(28)
            # Safeguard for lag features
            def get_lag(idx, default=0):
                try:
                    return last_28_days.iloc[idx]["quantity_sold"]
                except IndexError:
                    return default

            row = {
                "store_id": store,
                "menu_item_id": item,
                "sales_date": next_date,
                "day_of_week": next_date.weekday(),
                "month": next_date.month,
                "week_of_year": next_date.isocalendar().week,
                "is_weekend": 1 if next_date.weekday() >= 5 else 0,
                "lag_1": get_lag(-1),
                "lag_2": get_lag(-2),
                "lag_7": get_lag(-7),
                "lag_14": get_lag(-14),
                "rolling_avg_7": last_28_days["quantity_sold"].tail(7).mean() if len(last_28_days) >= 1 else 0,
                "rolling_avg_28": last_28_days["quantity_sold"].mean() if len(last_28_days) >= 1 else 0,
            }

            predictions.append(row)

        pred_df = pd.DataFrame(predictions)

        X_pred = pred_df[features]
        pred_df["predicted_quantity"] = model.predict(X_pred)

        temp = pred_df.rename(columns = {"predicted_quantity":"quantity_sold"})
        df = pd.concat([df, temp], ignore_index = True)

        results.append(pred_df)
    
    final_df = pd.concat(results).reset_index(drop=True)

    return final_df
