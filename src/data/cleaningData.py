import pandas as pd

# Load dataset
df = pd.read_csv("synthetic_daily_item_sales.csv", parse_dates = ["sales_date"])

# Sort chronologically per store and item
df = df.sort_values(["store_id", "menu_item_id", "sales_date"])

# Create Calendar Features: (Weekends != weekdays, December != Friday)
# Extract calendar signals from the date column and capture: Weekly seasonality, Monthly seasonality, Weekend behavior
df["day_of_week"] = df["sales_date"].dt.weekday
df["month"] = df["sales_date"].dt.month
df["week_of_year"] = df["sales_date"].dt.isocalendar().week.astype(int)
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

# Create Lag Features (Add Memory)
# lag_1 -> yesterdat
# lag_2 -> 2 days ago
# lag_7 -> same weekday last week
# lag_14 -> two weeks ago

group_cols = ["store_id", "menu_item_id"]

df["lag_1"]  = df.groupby(group_cols)["quantity_sold"].shift(1)
df["lag_2"]  = df.groupby(group_cols)["quantity_sold"].shift(2)
df["lag_7"]  = df.groupby(group_cols)["quantity_sold"].shift(7)
df["lag_14"] = df.groupby(group_cols)["quantity_sold"].shift(14)

# Create Rolling Averages: rolling_avg_7 = average from t-1 to t-7
df["rolling_avg_7"] = (
    df.groupby(group_cols)["quantity_sold"]
      .shift(1)
      .rolling(window=7)
      .mean()
)

df["rolling_avg_28"] = (
    df.groupby(group_cols)["quantity_sold"]
      .shift(1)
      .rolling(window=28)
      .mean()
)

# Remove Early Rows Without Enough History
df_model = df.dropna().reset_index(drop=True)