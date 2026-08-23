from fastapi.testclient import TestClient

from app.forecast_api import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_inventory_status():
    response = client.get("/inventory/status")

    assert response.status_code == 200
    assert response.json()["status"] == "active"


def test_forecast():
    payload = {
        "product_id": "P005",
        "day_of_week": 2,
        "day_of_month": 15,
        "month": 8,
        "revenue_per_unit": 25.5,
        "units_per_customer": 2.1,
        "lag_1": 21,
        "lag_7": 23,
        "rolling_mean_7": 22,
        "rolling_mean_30": 21.5,
        "current_inventory": 20,
    }

    response = client.post("/forecast", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == "P005"
    assert "predicted_units_sold" in data
    assert "forecast_lower" in data
    assert "forecast_upper" in data
    assert "inventory_risk" in data
    assert "recommended_reorder_quantity" in data

def test_forecast_rejects_negative_inventory():
    payload = {
        "product_id": "P005",
        "day_of_week": 2,
        "day_of_month": 15,
        "month": 8,
        "revenue_per_unit": 25.5,
        "units_per_customer": 2.1,
        "lag_1": 21,
        "lag_7": 23,
        "rolling_mean_7": 22,
        "rolling_mean_30": 21.5,
        "current_inventory": -10,
    }

    response = client.post("/forecast", json=payload)

    assert response.status_code == 422

def test_forecast_rejects_invalid_month():
    payload = {
        "product_id": "P005",
        "day_of_week": 2,
        "day_of_month": 15,
        "month": 13,
        "revenue_per_unit": 25.5,
        "units_per_customer": 2.1,
        "lag_1": 21,
        "lag_7": 23,
        "rolling_mean_7": 22,
        "rolling_mean_30": 21.5,
        "current_inventory": 20,
    }

    response = client.post("/forecast", json=payload)

    assert response.status_code == 422


def test_forecast_rejects_invalid_day_of_week():
    payload = {
        "product_id": "P005",
        "day_of_week": 7,
        "day_of_month": 15,
        "month": 8,
        "revenue_per_unit": 25.5,
        "units_per_customer": 2.1,
        "lag_1": 21,
        "lag_7": 23,
        "rolling_mean_7": 22,
        "rolling_mean_30": 21.5,
        "current_inventory": 20,
    }

    response = client.post("/forecast", json=payload)

    assert response.status_code == 422