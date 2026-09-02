from pathlib import Path

import pytest

from services.forecast_features import create_forecast_features


def test_create_forecast_features():
    file_path = Path("data/sales.csv")

    features = create_forecast_features(
        file_path,
        "P005",
        "2025-12-31",
    )

    expected_columns = [
        "product_id",
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
        assert column in features.columns

    assert len(features) == 1
    assert features.loc[0, "product_id"] == "P005"


def test_forecast_features_use_historical_data():
    file_path = Path("data/sales.csv")

    features = create_forecast_features(
        file_path,
        "P005",
        "2025-12-31",
    )

    assert features.loc[0, "lag_1"] == 85
    assert features.loc[0, "lag_7"] == 92


def test_unknown_product_raises_error():
    file_path = Path("data/sales.csv")

    with pytest.raises(ValueError, match="Product not found"):
        create_forecast_features(
            file_path,
            "BAD",
            "2025-12-31",
        )


def test_insufficient_history_raises_error():
    file_path = Path("data/sales.csv")

    with pytest.raises(
        ValueError,
        match="At least 30 days",
    ):
        create_forecast_features(
            file_path,
            "P005",
            "2025-01-15",
        )

def test_future_forecast_date():
    file_path = Path("data/sales.csv")

    features = create_forecast_features(
        file_path,
        "P005",
        "2026-01-01",
    )

    assert len(features) == 1
    assert features.loc[0, "product_id"] == "P005"
    assert features.loc[0, "day_of_month"] == 1
    assert features.loc[0, "month"] == 1