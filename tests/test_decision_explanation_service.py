
import pytest

from services.decision_explanation_service import explain_decision


def test_explain_emergency_sourcing():
    impact = {
        "impact_level": "HIGH",
        "expected_shortage": 150,
        "projected_inventory": -50,
    }

    decision = {
        "product_id": "P001",
        "recommended_action": "EMERGENCY_SOURCING",
        "priority": "CRITICAL",
    }

    result = explain_decision(impact, decision)

    assert result["recommended_action"] == "EMERGENCY_SOURCING"
    assert result["priority"] == "CRITICAL"
    assert result["supporting_evidence"]["expected_shortage"] == 150
    assert len(result["key_factors"]) == 3


def test_explain_alternative_supplier():
    impact = {
        "impact_level": "HIGH",
        "expected_shortage": 50,
        "projected_inventory": 10,
    }

    decision = {
        "product_id": "P002",
        "recommended_action": "ALTERNATIVE_SUPPLIER",
        "priority": "HIGH",
    }

    result = explain_decision(impact, decision)

    assert result["recommended_action"] == "ALTERNATIVE_SUPPLIER"
    assert result["priority"] == "HIGH"
    assert result["decision_summary"]


def test_explain_reorder():
    impact = {
        "impact_level": "MEDIUM",
        "expected_shortage": 20,
        "projected_inventory": 5,
    }

    decision = {
        "product_id": "P003",
        "recommended_action": "REORDER",
        "priority": "MEDIUM",
    }

    result = explain_decision(impact, decision)

    assert result["recommended_action"] == "REORDER"
    assert result["priority"] == "MEDIUM"


def test_explain_monitor():
    impact = {
        "impact_level": "LOW",
        "expected_shortage": 0,
        "projected_inventory": 100,
    }

    decision = {
        "product_id": "P004",
        "recommended_action": "MONITOR",
        "priority": "LOW",
    }

    result = explain_decision(impact, decision)

    assert result["recommended_action"] == "MONITOR"
    assert result["priority"] == "LOW"


def test_missing_impact_field():
    impact = {
        "impact_level": "HIGH",
        "expected_shortage": 150,
    }

    decision = {
        "product_id": "P001",
        "recommended_action": "EMERGENCY_SOURCING",
        "priority": "CRITICAL",
    }

    with pytest.raises(ValueError, match="projected_inventory"):
        explain_decision(impact, decision)


def test_unsupported_action():
    impact = {
        "impact_level": "LOW",
        "expected_shortage": 0,
        "projected_inventory": 100,
    }

    decision = {
        "product_id": "P005",
        "recommended_action": "UNKNOWN_ACTION",
        "priority": "LOW",
    }

    with pytest.raises(ValueError, match="Unsupported recommended action"):
        explain_decision(impact, decision)
