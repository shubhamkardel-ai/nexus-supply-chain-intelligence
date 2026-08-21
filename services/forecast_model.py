from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from sklearn.preprocessing import OneHotEncoder

from services.demand_features import create_demand_features


NUMERIC_FEATURES = [
    "day_of_week",
    "day_of_month",
    "month",
    "revenue_per_unit",
    "units_per_customer",
    "lag_1",
    "lag_7",
    "rolling_mean_7",
    "rolling_mean_30",
]

CATEGORICAL_FEATURES = [
    "product_id",
]


def prepare_data(file_path: Path):
    dataframe = create_demand_features(file_path)

    dataframe = dataframe.dropna(
        subset=NUMERIC_FEATURES
    ).reset_index(drop=True)

    dataframe = dataframe.sort_values("sale_date")

    split_index = int(len(dataframe) * 0.8)

    train_data = dataframe.iloc[:split_index]
    test_data = dataframe.iloc[split_index:]

    X_train = train_data[
        NUMERIC_FEATURES + CATEGORICAL_FEATURES
    ]

    X_test = test_data[
        NUMERIC_FEATURES + CATEGORICAL_FEATURES
    ]

    y_train = train_data["units_sold"]
    y_test = test_data["units_sold"]

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "product",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="passthrough",
    )

    X_train_encoded = preprocessor.fit_transform(X_train)

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train_encoded, y_train)

    return model, preprocessor

def predict_with_range(model, encoded_data):
    tree_predictions = [
        tree.predict(encoded_data)[0]
        for tree in model.estimators_
    ]

    prediction = model.predict(encoded_data)[0]

    lower_bound = pd.Series(tree_predictions).quantile(0.10)
    upper_bound = pd.Series(tree_predictions).quantile(0.90)

    return prediction, lower_bound, upper_bound


if __name__ == "__main__":
    file_path = Path("data/sales.csv")

    X_train, X_test, y_train, y_test = prepare_data(file_path)

    model, preprocessor = train_model(
        X_train,
        y_train,
    )

    X_test_encoded = preprocessor.transform(X_test)

    predictions = model.predict(X_test_encoded)

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = root_mean_squared_error(
        y_test,
        predictions,
    )

    print("Demand Forecasting Model")
    print("------------------------")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")