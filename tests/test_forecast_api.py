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
        "forecast_date": "2026-01-01",
        "current_inventory": 20,
    }

    response = client.post("/forecast", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == "P005"
    assert data["forecast_date"] == "2026-01-01"
    assert "predicted_units_sold" in data
    assert "forecast_lower" in data
    assert "forecast_upper" in data
    assert "forecast_type" in data
    assert "model" in data
    assert "inventory_risk" in data
    assert "current_inventory" in data
    assert "recommended_reorder_quantity" in data


def test_forecast_rejects_negative_inventory():
    payload = {
        "product_id": "P005",
        "forecast_date": "2026-01-01",
        "current_inventory": -10,
    }

    response = client.post("/forecast", json=payload)

    assert response.status_code == 422


def test_forecast_rejects_invalid_date():
    payload = {
        "product_id": "P005",
        "forecast_date": "not-a-date",
        "current_inventory": 20,
    }

    response = client.post("/forecast", json=payload)

    assert response.status_code == 422


def test_forecast_rejects_empty_product_id():
    payload = {
        "product_id": "",
        "forecast_date": "2026-01-01",
        "current_inventory": 20,
    }

    response = client.post("/forecast", json=payload)

    assert response.status_code == 422
def test_batch_forecast():
    payload = {
        "forecast_date": "2026-01-01",
        "forecasts": [
            {
                "product_id": "P005",
                "current_inventory": 20,
            },
            {
                "product_id": "P010",
                "current_inventory": 100,
            },
        ],
    }

    def test_forecast_report():
        response = client.get("/forecast/report")

        assert response.status_code == 200

        data = response.json()

        assert data["model"] == "Random Forest"
        assert data["training_samples"] == 5360
        assert data["testing_samples"] == 1340
        assert data["trees"] == 200
        assert data["mae"] >= 0
        assert data["rmse"] >= 0
        assert data["mape"] >= 0

    def test_forecast_report():
        response = client.get("/forecast/report")

        assert response.status_code == 200

        data = response.json()

        assert data["model"] == "Random Forest"
        assert data["training_samples"] == 5360
        assert data["testing_samples"] == 1340
        assert data["trees"] == 200
        assert data["mae"] >= 0
        assert data["rmse"] >= 0
        assert data["mape"] >= 0

    response = client.post("/forecast/batch", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "forecasts" in data
    assert len(data["forecasts"]) == 2

    for forecast in data["forecasts"]:
        assert "product_id" in forecast
        assert "predicted_units_sold" in forecast
        assert "forecast_lower" in forecast
        assert "forecast_upper" in forecast
        assert "inventory_risk" in forecast
        assert "recommended_reorder_quantity" in forecast

def test_batch_forecast_rejects_empty_forecasts():
    payload = {
        "forecast_date": "2026-01-01",
        "forecasts": [],
    }

    response = client.post("/forecast/batch", json=payload)

    assert response.status_code == 422


def test_batch_forecast_rejects_negative_inventory():
    payload = {
        "forecast_date": "2026-01-01",
        "forecasts": [
            {
                "product_id": "P005",
                "current_inventory": -10,
            },
        ],
    }

    response = client.post("/forecast/batch", json=payload)

    assert response.status_code == 422


def test_batch_forecast_rejects_empty_product_id():
    payload = {
        "forecast_date": "2026-01-01",
        "forecasts": [
            {
                "product_id": "",
                "current_inventory": 20,
            },
        ],
    }

    response = client.post("/forecast/batch", json=payload)

    assert response.status_code == 422

def test_forecast_report():
    response = client.get("/forecast/report")

    assert response.status_code == 200

    data = response.json()

    assert data["model"] == "Random Forest"
    assert data["training_samples"] == 5360
    assert data["testing_samples"] == 1340
    assert data["trees"] == 200
    assert data["mae"] >= 0
    assert data["rmse"] >= 0
    assert data["mape"] >= 0