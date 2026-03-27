import pandas as pd

def compute_ingredient_demand(predictions_df, recipes_df):
    
    # Merge predictions with recipes
    merged = predictions_df.merge(
        recipes_df,
        on="menu_item_id",
        how="left"
    )
    
    # Compute ingredient quantity
    merged["ingredient_quantity"] = (
        merged["predicted_quantity"] * merged["quantity"]
    )

    # Aggregate per store + ingredient
    ingredient_demand = (
        merged
        .groupby(["store_id", "ingredient_id", "sales_date"])
        ["ingredient_quantity"]
        .sum()
        .reset_index()
    )

    return ingredient_demand