import pandas as pd
from pathlib import Path

from services.demand_features import create_demand_features

def test_demand_features_created():
    file_path = Path("data/sales.csv")

    dataframe = create_demand_features(file_path)

    expected_columns = [
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

    for column in expected_columns:
        assert column in dataframe.columns


def test_lag_features_use_previous_demand():
    file_path = Path("data/sales.csv")

    dataframe = create_demand_features(file_path)

    product_data = dataframe[
        dataframe["product_id"] == "P001"
    ].reset_index(drop=True)

    assert product_data.loc[1, "lag_1"] == product_data.loc[0, "units_sold"]
    assert product_data.loc[7, "lag_7"] == product_data.loc[0, "units_sold"]


def test_rolling_features_use_historical_data_only():
    file_path = Path("data/sales.csv")

    dataframe = create_demand_features(file_path)

    product_data = dataframe[
        dataframe["product_id"] == "P001"
    ].reset_index(drop=True)

    assert pd.isna(product_data.loc[0, "rolling_mean_7"])
    assert pd.isna(product_data.loc[29, "rolling_mean_30"])

    assert not pd.isna(product_data.loc[30, "rolling_mean_30"])