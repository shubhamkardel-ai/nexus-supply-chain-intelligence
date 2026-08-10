from pathlib import Path

import pandas as pd

from services.data_loader import load_csv


def calculate_demand_statistics(file_path: Path) -> pd.DataFrame:
    """
    Calculate demand statistics for each product.
    """
    dataframe = load_csv(file_path)

    statistics = (
        dataframe.groupby("product_id")
        .agg(
            total_units_sold=("units_sold", "sum"),
            average_units_sold=("units_sold", "mean"),
            maximum_units_sold=("units_sold", "max"),
            minimum_units_sold=("units_sold", "min"),
            total_revenue=("revenue", "sum"),
        )
        .reset_index()
    )

    return statistics


if __name__ == "__main__":
    file_path = Path("data/sales.csv")

    statistics = calculate_demand_statistics(file_path)

    print("\nDemand Statistics:")
    print(statistics)