import pandas as pd

'''
    Responsabilities of this class:
        - validate required columns
        - parse types 
        - drop bad rows
        - aggregate duplicates
'''

REQUIRED_COLUMNS = {"store_id", "menu_item_id", "sales_date", "quantity_sold"}

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
        Clean raw sales date and ensure one row per store/item/day
    """
    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    cleaned = df.copy()

    cleaned["sales_date"] = pd.to_datetime(cleaned["sales_date"], errors="coerce")
    cleaned["quantity_sold"] = pd.to_numeric(cleaned["quantity_sold"], errors="coerce")

    cleaned = cleaned.dropna(
        subset = ["store_id", "menu_item_id", "sales_date", "quantity_sold"]
    ).copy()

    cleaned = cleaned[cleaned["quantity_sold"] >= 0].copy()

    cleaned["store_id"] = cleaned["store_id"].astype(str)
    cleaned["menu_item_id"] = cleaned["menu_item_id"].astype(str)

    cleaned = (
        cleaned.groupby(["store_id", "menu_item_id", "sales_date"], as_index = False)["quantity_sold"]
        .sum()
    )

    return cleaned
