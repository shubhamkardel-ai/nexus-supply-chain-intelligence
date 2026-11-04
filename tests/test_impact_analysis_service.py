from services.impact_analysis_service import analyze_disruption_impact


def test_high_impact_with_shortage():
    simulation_result = {
        "product_id": "P001",
        "disruption_type": "supplier_delay",
        "expected_shortage": 100,
        "projected_inventory": 0,
        "risk_level": "HIGH",
    }

    result = analyze_disruption_impact(simulation_result)

    assert result["impact_level"] == "HIGH"
    assert "Urgent replenishment" in result["recommendation"]


def test_medium_impact():
    simulation_result = {
        "product_id": "P001",
        "disruption_type": "demand_spike",
        "expected_shortage": 0,
        "projected_inventory": 15,
        "risk_level": "MEDIUM",
    }

    result = analyze_disruption_impact(simulation_result)

    assert result["impact_level"] == "MEDIUM"
    assert "Monitor inventory" in result["recommendation"]


def test_high_impact_inventory_depletion():
    simulation_result = {
        "product_id": "P002",
        "disruption_type": "inventory_shortage",
        "expected_shortage": 0,
        "projected_inventory": 0,
        "risk_level": "LOW",
    }

    result = analyze_disruption_impact(simulation_result)

    assert result["impact_level"] == "HIGH"
    assert "Inventory depletion" in result["recommendation"]


def test_low_impact():
    simulation_result = {
        "product_id": "P003",
        "disruption_type": "supplier_delay",
        "expected_shortage": 0,
        "projected_inventory": 200,
        "risk_level": "LOW",
    }

    result = analyze_disruption_impact(simulation_result)

    assert result["impact_level"] == "LOW"
    assert "stable" in result["recommendation"]