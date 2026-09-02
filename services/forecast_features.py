from pathlib import Path

import pandas as pd

from services.data_loader import load_csv


def create_forecast_features(
    file_path: Path,
    product_id: str,
    forecast_date: str,
) -> pd.DataFrame:
    """
    Create model-ready features for a future demand forecast.

    Features are calculated using historical data only.
    """

    dataframe = load_csv(file_path)

    dataframe["sale_date"] = pd.to_datetime(
        dataframe["sale_date"]
    )

    dataframe = dataframe.sort_values(
        ["product_id", "sale_date"]
    ).reset_index(drop=True)

    product_data = dataframe[
        dataframe["product_id"] == product_id
    ].copy()

    if product_data.empty:
        raise ValueError(
            f"Product not found: {product_id}"
        )

    forecast_date = pd.Timestamp(forecast_date)

    historical_data = product_data[
        product_data["sale_date"] < forecast_date
    ].copy()

    if len(historical_data) < 30:
        raise ValueError(
            "At least 30 days of historical data are required."
        )

    features = pd.DataFrame(
        [
            {
                "product_id": product_id,
                "day_of_week": forecast_date.dayofweek,
                "day_of_month": forecast_date.day,
                "month": forecast_date.month,
                "revenue_per_unit": (
                    historical_data["revenue"]
                    .tail(7)
                    .mean()
                ),
                "units_per_customer": (
                    historical_data["customer_count"]
                    .tail(7)
                    .mean()
                ),
                "lag_1": historical_data["units_sold"].iloc[-1],
                "lag_7": historical_data["units_sold"].iloc[-7],
                "rolling_mean_7": (
                    historical_data["units_sold"]
                    .tail(7)
                    .mean()
                ),
                "rolling_mean_30": (
                    historical_data["units_sold"]
                    .tail(30)
                    .mean()
                ),
            }
        ]
    )

    return features