from pathlib import Path

import pandas as pd

from services.demand_features import create_demand_features
from services.forecast_model import (
    prepare_data,
    train_model,
)
from services.model_evaluation import evaluate_model


def generate_forecast_report(file_path: Path) -> dict:
    """
    Generate a performance report for the demand forecasting model.
    """

    X_train, X_test, y_train, y_test = prepare_data(file_path)

    model, preprocessor = train_model(
        X_train,
        y_train,
    )

    X_test_encoded = preprocessor.transform(X_test)

    predictions = model.predict(X_test_encoded)

    metrics = evaluate_model(
        y_test,
        predictions,
    )

    return {
        "model": "Random Forest",
        "training_samples": len(X_train),
        "testing_samples": len(X_test),
        "trees": len(model.estimators_),
        "mae": round(float(metrics["mae"]), 2),
        "rmse": round(float(metrics["rmse"]), 2),
        "mape": round(float(metrics["mape"]), 2),
    }


if __name__ == "__main__":
    file_path = Path("data/sales.csv")

    report = generate_forecast_report(file_path)

    print("\nForecast Performance Report")
    print("---------------------------")

    for key, value in report.items():
        print(f"{key}: {value}")