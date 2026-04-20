
from data import load_data, split_data, load_recipes, load_inventory
from features import build_features, compute_ingredient_demand, compute_order_quantity

from models import train_model, make_predictions, predict_next_day, predict_next_7_days
from evaluation import evaluate_model


def main():
    # 1. Load
    df = load_data()

    # 2. Feature engineering
    df_model = build_features(df)

    # 3. Define features
    features = [
        "day_of_week",
        "month",
        "week_of_year",
        "is_weekend",
        "lag_1",
        "lag_2",
        "lag_7",
        "lag_14",
        "rolling_avg_7",
        "rolling_avg_28"
    ]

    X = df_model[features]
    y = df_model["quantity_sold"]

    # 4. Split
    X_train, X_test, y_train, y_test, train, test = split_data(df_model, features)

    # 5. Debug prints
    print("Data loaded successfully.")
    print("Shape of full dataset:", df.shape)
    print("Shape after feature engineering:", df_model.shape)
    print("Train shape:", train.shape)
    print("Test shape:", test.shape)

    print("\nFirst 5 rows of engineered dataset:")
    print(df_model.head())

    # 6. Train model
    model = train_model(X_train, y_train)

    # 7. Predict
    predictions = make_predictions(model, X_test)

    # 8. Evaluate
    results = evaluate_model(y_test, predictions)

    # 9. Debug prints
    print("Model Performance: ", results)

    # 10. Predict next day
    #next_day_predictions = predict_next_day(df_model, model, features)
    next_day_predictions = predict_next_7_days(df_model, model, features, days=7)
    print("\nNext Day Predictions: ")
    print(next_day_predictions.head())

    # 11. Load recipes
    recipes_df = load_recipes()

    # 12. Compute Ingredient Demand
    ingredient_forecast = compute_ingredient_demand(
        next_day_predictions,
        recipes_df
    )
    ingredient_forecast["ingredient_quantity"] = ingredient_forecast["ingredient_quantity"].round(2)
    print ("\nIngredient Forecast:")
    print(ingredient_forecast.head())

    # 13. Load inventory
    inventory_df = load_inventory()

    # 14. Compute order quantities
    order_plan = compute_order_quantity(
        ingredient_forecast,
        inventory_df,
        safety_factor=0.1
    )

    print("\nOrder Plan:")
    print(order_plan.head())

if __name__ == "__main__":
    main()