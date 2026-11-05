
import pytest

from services.supplier_service import create_supplier
from services.supply_chain_optimizer import optimize_supplier_selection


def test_selects_best_supplier_using_cost_reliability_and_lead_time():
    suppliers = [
        create_supplier(
            supplier_id="S001",
            name="Supplier One",
            country="India",
            lead_time_days=10,
            reliability_score=90,
            unit_cost=100,
            capacity=1000,
            minimum_order_quantity=10,
        ),
        create_supplier(
            supplier_id="S002",
            name="Supplier Two",
            country="India",
            lead_time_days=5,
            reliability_score=95,
            unit_cost=110,
            capacity=1000,
            minimum_order_quantity=10,
        ),
        create_supplier(
            supplier_id="S003",
            name="Supplier Three",
            country="India",
            lead_time_days=15,
            reliability_score=70,
            unit_cost=90,
            capacity=1000,
            minimum_order_quantity=10,
        ),
    ]

    result = optimize_supplier_selection(
        suppliers,
        required_quantity=100,
    )

    assert result["supplier_id"] == "S002"
    assert result["total_cost"] == 11000
    assert result["required_quantity"] == 100


def test_excludes_supplier_with_insufficient_capacity():
    suppliers = [
        create_supplier(
            supplier_id="S001",
            name="Too Small",
            country="India",
            lead_time_days=3,
            reliability_score=99,
            unit_cost=1,
            capacity=50,
            minimum_order_quantity=1,
        ),
        create_supplier(
            supplier_id="S002",
            name="Can Supply",
            country="India",
            lead_time_days=6,
            reliability_score=90,
            unit_cost=10,
            capacity=200,
            minimum_order_quantity=1,
        ),
    ]

    result = optimize_supplier_selection(
        suppliers,
        required_quantity=100,
    )

    assert result["supplier_id"] == "S002"


def test_excludes_supplier_when_order_is_below_minimum_quantity():
    suppliers = [
        create_supplier(
            supplier_id="S001",
            name="High MOQ",
            country="India",
            lead_time_days=3,
            reliability_score=99,
            unit_cost=1,
            capacity=500,
            minimum_order_quantity=150,
        ),
        create_supplier(
            supplier_id="S002",
            name="Eligible",
            country="India",
            lead_time_days=6,
            reliability_score=90,
            unit_cost=10,
            capacity=200,
            minimum_order_quantity=10,
        ),
    ]

    result = optimize_supplier_selection(
        suppliers,
        required_quantity=100,
    )

    assert result["supplier_id"] == "S002"


def test_raises_error_when_no_supplier_is_eligible():
    suppliers = [
        create_supplier(
            supplier_id="S001",
            name="Too Small",
            country="India",
            lead_time_days=3,
            reliability_score=99,
            unit_cost=1,
            capacity=50,
            minimum_order_quantity=1,
        )
    ]

    with pytest.raises(ValueError, match="No supplier can fulfill"):
        optimize_supplier_selection(
            suppliers,
            required_quantity=100,
        )


def test_rejects_zero_or_negative_required_quantity():
    suppliers = []

    with pytest.raises(ValueError, match="Required quantity"):
        optimize_supplier_selection(suppliers, required_quantity=0)

    with pytest.raises(ValueError, match="Required quantity"):
        optimize_supplier_selection(suppliers, required_quantity=-5)
