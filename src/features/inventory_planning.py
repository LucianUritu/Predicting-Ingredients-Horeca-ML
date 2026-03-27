import pandas as pd

def compute_order_quantity(ingredient_forecast, inventory_df, safety_factor=0.1):
    """
        Compute how much to order per ingredient
    """

    # Merge forecast with inventory
    merged = ingredient_forecast.merge(
        inventory_df,
        on=["store_id", "ingredient_id"],
        how="left"
    )

    # Fill missing stock with 0
    merged["current_stock"] = merged["current_stock"].fillna(0)

    # Add safety buffer
    merged["buffer"] = merged["ingredient_quantity"] * safety_factor

    # Compute order quantity
    merged["order_quantity"] = (
        merged["ingredient_quantity"] + 
        merged["buffer"] -
        merged["current_stock"]
    )

    # Prevent negative orders
    merged["order_quantity"] = merged["order_quantity"].clip(lower=0)

    return merged[[
        "store_id",
        "ingredient_id",
        "sales_date",
        "ingredient_quantity",
        "current_stock",
        "buffer",
        "order_quantity"
    ]]
