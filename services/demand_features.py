from pathlib import Path

import pandas as pd

from services.data_loader import load_csv


def create_demand_features(file_path: Path) -> pd.DataFrame:
    """
    Create time-based and demand-related features.
    """
    dataframe = load_csv(file_path)

    dataframe["sale_date"] = pd.to_datetime(dataframe["sale_date"])

    dataframe["day_of_week"] = dataframe["sale_date"].dt.dayofweek
    dataframe["day_of_month"] = dataframe["sale_date"].dt.day
    dataframe["month"] = dataframe["sale_date"].dt.month

    dataframe["revenue_per_unit"] = (
        dataframe["revenue"] / dataframe["units_sold"]
    )

    dataframe["units_per_customer"] = (
        dataframe["units_sold"] / dataframe["customer_count"]
    )

    return dataframe


if __name__ == "__main__":
    file_path = Path("data/sales.csv")

    features = create_demand_features(file_path)

    print("\nDemand Features:")
    print(features)