
from data import load_data, split_data
from features import build_features

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


if __name__ == "__main__":
    main()