from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from services.data_loader import load_csv
from services.forecast_model import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    predict_with_range,
)


def generate_multi_day_forecast(
    file_path: Path,
    product_id: str,
    start_date: date,
    horizon: int,
    model,
    preprocessor,
) -> list[dict]:
    if horizon < 1:
        raise ValueError("Forecast horizon must be at least 1 day.")

    dataframe = load_csv(file_path)

    dataframe["sale_date"] = pd.to_datetime(dataframe["sale_date"])

    product_data = dataframe[
        dataframe["product_id"] == product_id
    ].copy()

    if product_data.empty:
        raise ValueError(f"Product not found: {product_id}")

    product_data = product_data.sort_values("sale_date")

    historical_data = product_data[
        product_data["sale_date"] < pd.Timestamp(start_date)
    ].copy()

    if len(historical_data) < 30:
        raise ValueError(
            "At least 30 days of historical data are required."
        )

    units_history = historical_data["units_sold"].tolist()

    revenue_per_unit = historical_data["revenue"].tail(7).mean()
    units_per_customer = (
        historical_data["customer_count"].tail(7).mean()
    )

    forecasts = []

    for day_offset in range(horizon):
        forecast_date = start_date + timedelta(days=day_offset)

        features = pd.DataFrame(
            [
                {
                    "product_id": product_id,
                    "day_of_week": forecast_date.weekday(),
                    "day_of_month": forecast_date.day,
                    "month": forecast_date.month,
                    "revenue_per_unit": revenue_per_unit,
                    "units_per_customer": units_per_customer,
                    "lag_1": units_history[-1],
                    "lag_7": units_history[-7],
                    "rolling_mean_7": (
                        sum(units_history[-7:]) / 7
                    ),
                    "rolling_mean_30": (
                        sum(units_history[-30:]) / 30
                    ),
                }
            ]
        )

        features = features[
            NUMERIC_FEATURES + CATEGORICAL_FEATURES
        ]

        encoded_data = preprocessor.transform(features)

        prediction, lower_bound, upper_bound = predict_with_range(
            model,
            encoded_data,
        )

        prediction = max(0.0, float(prediction))
        lower_bound = max(0.0, float(lower_bound))
        upper_bound = max(0.0, float(upper_bound))

        forecasts.append(
            {
                "forecast_date": forecast_date,
                "predicted_units_sold": round(prediction, 2),
                "forecast_lower": round(lower_bound, 2),
                "forecast_upper": round(upper_bound, 2),
            }
        )

        units_history.append(prediction)

    return forecasts