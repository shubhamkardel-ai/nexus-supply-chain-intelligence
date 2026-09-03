from pathlib import Path

from services.forecast_report import generate_forecast_report


def test_generate_forecast_report():
    file_path = Path("data/sales.csv")

    report = generate_forecast_report(file_path)

    assert report["model"] == "Random Forest"
    assert report["training_samples"] == 5360
    assert report["testing_samples"] == 1340
    assert report["trees"] == 200


def test_forecast_report_metrics_are_valid():
    file_path = Path("data/sales.csv")

    report = generate_forecast_report(file_path)

    assert report["mae"] >= 0
    assert report["rmse"] >= 0
    assert report["mape"] >= 0