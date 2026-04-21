import pandas as pd

"""
    Responsibility:
        Remove items with too little history
"""
def filter_items_by_min_history(df: pd.DataFrame,
                                min_days_per_item: int = 30,) -> pd.DataFrame:
    """
    Keep only items that have at least `min_days_per_item`
    daily observations in the expanded time series.
    """
    if df.empty:
        return df.copy()

    item_counts = (
        df.groupby("menu_item_id")["sales_date"]
        .count()
        .reset_index(name="num_days")
    )

    valid_items = item_counts.loc[
        item_counts["num_days"] >= min_days_per_item, "menu_item_id"
    ]

    filtered = df[df["menu_item_id"].isin(valid_items)].copy()

    return filtered.sort_values(
        ["store_id", "menu_item_id", "sales_date"]
    ).reset_index(drop=True)