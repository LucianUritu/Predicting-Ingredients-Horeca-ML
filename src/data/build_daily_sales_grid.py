import pandas as pd

"""
    Responsibility:
        - create continuous daily time series
        - fill missing days with zero sales 
"""

def build_daily_sales_grid(df: pd.DataFrame) -> pd.DataFrame:
    """
        Expand cleaned sales data into a full daily time series
        for each real store-item pair.
        Missing days are filled with zero quantity_sold.
    """

    if df.empty:
        return df.copy()
    
    min_date = df["sales_date"].min()
    max_date = df["sales_date"].max()
    all_dates = pd.date_range(min_date, max_date, freq="D")

    store_item_pairs = df[["store_id", "menu_item_id"]].drop_duplicates().copy()
    store_item_pairs["key"] = 1

    dates_df = pd.DataFrame({"sales_date": all_dates, "key": 1})

    full_grid = store_item_pairs.merge(dates_df, on="key").drop(columns="key")

    full_grid = full_grid.merge(
        df,
        on=["store_id", "menu_item_id", "sales_date"],
        how="left",
    )

    full_grid["quantity_sold"] = full_grid["quantity_sold"].fillna(0)

    return full_grid.sort_values(
        ["store_id", "menu_item_id", "sales_date"]
    ).reset_index(drop=True)