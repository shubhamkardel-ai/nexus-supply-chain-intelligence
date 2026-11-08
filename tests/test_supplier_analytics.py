
import pytest

from models.supplier import Supplier
from services.supplier_analytics import generate_supplier_analytics


@pytest.fixture
def suppliers():
    return [
        Supplier(
            supplier_id="S001",
            name="Alpha Supplies",
            country="India",
            lead_time_days=5,
            reliability_score=95,
            risk_level="LOW",
            unit_cost=120,
            capacity=500,
            minimum_order_quantity=50,
        ),
        Supplier(
            supplier_id="S002",
            name="Beta Supplies",
            country="India",
            lead_time_days=3,
            reliability_score=90,
            risk_level="LOW",
            unit_cost=125,
            capacity=300,
            minimum_order_quantity=100,
        ),
        Supplier(
            supplier_id="S003",
            name="Gamma Supplies",
            country="India",
            lead_time_days=8,
            reliability_score=98,
            risk_level="MEDIUM",
            unit_cost=110,
            capacity=1000,
            minimum_order_quantity=200,
        ),
    ]


@pytest.fixture
def rankings():
    return [
        {
            "supplier_id": "S001",
            "supplier_name": "Alpha Supplies",
            "total_cost": 12000,
            "lead_time_days": 5,
            "reliability_score": 95,
            "optimization_score": 0.20,
            "rank": 1,
        },
        {
            "supplier_id": "S002",
            "supplier_name": "Beta Supplies",
            "total_cost": 12500,
            "lead_time_days": 3,
            "reliability_score": 90,
            "optimization_score": 0.35,
            "rank": 2,
        },
    ]


def test_cost_analysis(suppliers, rankings):
    result = generate_supplier_analytics(
        suppliers, 100, rankings
    )

    cost = result["cost_analysis"]

    assert cost["lowest_cost_supplier"]["supplier_id"] == "S001"
    assert cost["highest_cost_supplier"]["supplier_id"] == "S002"
    assert cost["cost_difference"] == 500


def test_performance_analysis(suppliers, rankings):
    result = generate_supplier_analytics(
        suppliers, 100, rankings
    )

    performance = result["performance_analysis"]

    assert performance["fastest_supplier"]["supplier_id"] == "S002"
    assert performance["most_reliable_supplier"]["supplier_id"] == "S001"


def test_eligibility_analysis(suppliers, rankings):
    result = generate_supplier_analytics(
        suppliers, 100, rankings
    )

    eligibility = result["eligibility_analysis"]

    assert eligibility["eligible_count"] == 2
    assert eligibility["excluded_count"] == 1

    excluded = next(
        item for item in eligibility["supplier_details"]
        if item["supplier_id"] == "S003"
    )

    assert excluded["eligible"] is False
    assert "Order quantity is below supplier minimum" in excluded["reasons"]


def test_recommendation_explanation(suppliers, rankings):
    result = generate_supplier_analytics(
        suppliers, 100, rankings
    )

    explanation = result["recommendation_explanation"]

    assert explanation["recommended_supplier"] == "Alpha Supplies"
    assert len(explanation["reasons"]) > 0
    assert len(explanation["trade_offs"]) > 0


def test_rejects_zero_quantity(suppliers, rankings):
    with pytest.raises(ValueError):
        generate_supplier_analytics(suppliers, 0, rankings)


def test_rejects_empty_suppliers(rankings):
    with pytest.raises(ValueError):
        generate_supplier_analytics([], 100, rankings)


def test_rejects_empty_rankings(suppliers):
    with pytest.raises(ValueError):
        generate_supplier_analytics(suppliers, 100, [])
