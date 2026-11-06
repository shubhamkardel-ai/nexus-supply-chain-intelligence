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

def test_forecast_includes_inventory_planning():
    response = client.post(
        "/forecast",
        json={
            "product_id": "P001",
            "forecast_date": "2025-12-31",
            "current_inventory": 20,
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert "safety_stock" in result
    assert "reorder_point" in result

def test_supplier_comparison():
    payload = {
        "required_quantity": 100,
        "suppliers": [
            {
                "supplier_id": "SUP001",
                "name": "Alpha Suppliers",
                "country": "India",
                "lead_time_days": 5,
                "reliability_score": 95,
                "unit_cost": 120,
                "capacity": 500,
                "minimum_order_quantity": 50,
                "contact_email": "alpha@example.com",
            },
            {
                "supplier_id": "SUP002",
                "name": "Beta Suppliers",
                "country": "India",
                "lead_time_days": 3,
                "reliability_score": 90,
                "unit_cost": 125,
                "capacity": 300,
                "minimum_order_quantity": 100,
                "contact_email": "beta@example.com",
            },
            {
                "supplier_id": "SUP003",
                "name": "Gamma Suppliers",
                "country": "Germany",
                "lead_time_days": 8,
                "reliability_score": 98,
                "unit_cost": 110,
                "capacity": 1000,
                "minimum_order_quantity": 200,
                "contact_email": "gamma@example.com",
            },
        ],
    }

    response = client.post("/suppliers/compare", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["required_quantity"] == 100

    assert data["recommended_supplier"]["supplier_id"] == "SUP001"

    rankings = data["supplier_rankings"]

    assert len(rankings) == 2
    assert rankings[0]["rank"] == 1
    assert rankings[1]["rank"] == 2

    assert rankings[0]["supplier_id"] == "SUP001"
    assert rankings[1]["supplier_id"] == "SUP002"

    assert rankings[0]["total_cost"] == 12000
    assert rankings[1]["total_cost"] == 12500