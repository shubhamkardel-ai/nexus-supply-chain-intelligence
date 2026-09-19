from services.supply_risk_service import (
    calculate_demand_risk,
    calculate_supply_risk,
)


def test_high_demand_risk():
    assert calculate_demand_risk(
        current_inventory=20,
        predicted_demand=30,
    ) == "HIGH"


def test_medium_demand_risk():
    assert calculate_demand_risk(
        current_inventory=32,
        predicted_demand=30,
    ) == "MEDIUM"


def test_low_demand_risk():
    assert calculate_demand_risk(
        current_inventory=50,
        predicted_demand=30,
    ) == "LOW"


def test_supply_risk():
    result = calculate_supply_risk(
        product_id="P001",
        supplier_id="S001",
        current_inventory=20,
        predicted_demand=30,
        supplier_risk="HIGH",
    )

    assert result.product_id == "P001"
    assert result.supplier_id == "S001"
    assert result.demand_risk == "HIGH"
    assert result.supplier_risk == "HIGH"
    assert result.overall_risk == "HIGH"
    assert result.risk_score == 80.0