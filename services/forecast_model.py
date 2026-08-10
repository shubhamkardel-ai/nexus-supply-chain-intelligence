from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

from services.demand_features import create_demand_features


def prepare_data(file_path: Path):
    dataframe = create_demand_features(file_path)

    dataframe = dataframe.sort_values("sale_date")

    feature_columns = [
        "day_of_week",
        "day_of_month",
        "month",
        "revenue_per_unit",
        "units_per_customer",
    ]

    X = dataframe[feature_columns]
    y = dataframe["units_sold"]

    split_index = int(len(dataframe) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    file_path = Path("data/sales.csv")

    X_train, X_test, y_train, y_test = prepare_data(file_path)

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = root_mean_squared_error(y_test, predictions)

    print("Model training completed!")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")