from fastapi.testclient import TestClient

from app.forecast_api import app


client = TestClient(app)


def test_multi_day_forecast_api():
    response = client.post(
        "/forecast/multi-day",
        json={
            "product_id": "P005",
            "start_date": "2026-01-01",
            "horizon": 7,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == "P005"
    assert data["start_date"] == "2026-01-01"
    assert data["horizon"] == 7

    assert len(data["forecasts"]) == 7

    for forecast in data["forecasts"]:
        assert "forecast_date" in forecast
        assert "predicted_units_sold" in forecast
        assert "forecast_lower" in forecast
        assert "forecast_upper" in forecast


def test_multi_day_forecast_api_invalid_horizon():
    response = client.post(
        "/forecast/multi-day",
        json={
            "product_id": "P005",
            "start_date": "2026-01-01",
            "horizon": 0,
        },
    )

    assert response.status_code == 422