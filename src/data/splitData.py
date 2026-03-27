
import pandas as pd

def split_data(df, features):
    cutoff_date = df["sales_date"].max() - pd.Timedelta(days=30)

    train = df[df["sales_date"] <= cutoff_date]
    test  = df[df["sales_date"] > cutoff_date]

    X_train = train[features]
    y_train = train["quantity_sold"]

    X_test = test[features]
    y_test = test["quantity_sold"]

    return X_train, X_test, y_train, y_test, train, test