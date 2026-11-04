from services.decision_engine import generate_decision


def test_critical_shortage_uses_emergency_sourcing():
    impact_result = {
        "product_id": "P001",
        "disruption_type": "supplier_unavailable",
        "impact_level": "HIGH",
        "expected_shortage": 150,
        "projected_inventory": 0,
    }

    result = generate_decision(impact_result)

    assert result["recommended_action"] == "EMERGENCY_SOURCING"
    assert result["priority"] == "CRITICAL"


def test_high_impact_uses_alternative_supplier():
    impact_result = {
        "product_id": "P002",
        "disruption_type": "supplier_delay",
        "impact_level": "HIGH",
        "expected_shortage": 50,
        "projected_inventory": 10,
    }

    result = generate_decision(impact_result)

    assert result["recommended_action"] == "ALTERNATIVE_SUPPLIER"
    assert result["priority"] == "HIGH"


def test_medium_impact_recommends_reorder():
    impact_result = {
        "product_id": "P003",
        "disruption_type": "demand_spike",
        "impact_level": "MEDIUM",
        "expected_shortage": 0,
        "projected_inventory": 20,
    }

    result = generate_decision(impact_result)

    assert result["recommended_action"] == "REORDER"
    assert result["priority"] == "MEDIUM"


def test_low_impact_recommends_monitoring():
    impact_result = {
        "product_id": "P004",
        "disruption_type": "supplier_delay",
        "impact_level": "LOW",
        "expected_shortage": 0,
        "projected_inventory": 200,
    }

    result = generate_decision(impact_result)

    assert result["recommended_action"] == "MONITOR"
    assert result["priority"] == "LOW"