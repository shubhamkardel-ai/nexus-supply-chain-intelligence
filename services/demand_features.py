from pathlib import Path

import pandas as pd

from services.data_loader import load_csv


def create_demand_features(file_path: Path) -> pd.DataFrame:
    """
    Create leakage-safe features for demand forecasting.
    """
    dataframe = load_csv(file_path)

    dataframe["sale_date"] = pd.to_datetime(dataframe["sale_date"])

    dataframe = dataframe.sort_values(
        ["product_id", "sale_date"]
    ).reset_index(drop=True)

    # Calendar features
    dataframe["day_of_week"] = dataframe["sale_date"].dt.dayofweek
    dataframe["day_of_month"] = dataframe["sale_date"].dt.day
    dataframe["month"] = dataframe["sale_date"].dt.month

    # Business features
    # Use historical information only to avoid target leakage.

    dataframe["revenue_per_unit"] = (
        dataframe.groupby("product_id")["revenue"]
        .transform(
            lambda series: series.shift(1).rolling(7).mean()
        )
    )

    dataframe["units_per_customer"] = (
        dataframe.groupby("product_id")["customer_count"]
        .transform(
            lambda series: series.shift(1).rolling(7).mean()
        )
    )

    # Historical demand features
    dataframe["lag_1"] = (
        dataframe.groupby("product_id")["units_sold"]
        .shift(1)
    )

    dataframe["lag_7"] = (
        dataframe.groupby("product_id")["units_sold"]
        .shift(7)
    )

    dataframe["rolling_mean_7"] = (
        dataframe.groupby("product_id")["units_sold"]
        .transform(
            lambda series: series.shift(1).rolling(7).mean()
        )
    )

    dataframe["rolling_mean_30"] = (
        dataframe.groupby("product_id")["units_sold"]
        .transform(
            lambda series: series.shift(1).rolling(30).mean()
        )
    )

    return dataframe


if __name__ == "__main__":
    file_path = Path("data/sales.csv")

    features = create_demand_features(file_path)

    print("\nDemand Features:")
    print(features.head(40))