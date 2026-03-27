
def build_features(df):
    df = df.sort_values(["store_id", "menu_item_id", "sales_date"])

    # Calendar features
    df["day_of_week"] = df["sales_date"].dt.weekday
    df["month"] = df["sales_date"].dt.month
    df["week_of_year"] = df["sales_date"].dt.isocalendar().week.astype(int)
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    group_cols = ["store_id", "menu_item_id"]

    # Lag features
    df["lag_1"]  = df.groupby(group_cols)["quantity_sold"].shift(1)
    df["lag_2"]  = df.groupby(group_cols)["quantity_sold"].shift(2)
    df["lag_7"]  = df.groupby(group_cols)["quantity_sold"].shift(7)
    df["lag_14"] = df.groupby(group_cols)["quantity_sold"].shift(14)

    # Rolling features
    df["rolling_avg_7"] = (
        df.groupby(group_cols)["quantity_sold"]
          .shift(1)
          .rolling(7)
          .mean()
    )

    df["rolling_avg_28"] = (
        df.groupby(group_cols)["quantity_sold"]
          .shift(1)
          .rolling(28)
          .mean()
    )

    df = df.dropna().reset_index(drop=True)

    return df