from services.inventory_service import (
    calculate_inventory_risk,
    calculate_reorder_quantity,
    get_inventory_recommendation,
)


def test_high_inventory_risk():
    result = calculate_inventory_risk(
        product_id="P001",
        current_inventory=20,
        predicted_demand=25,
    )

    assert result.inventory_risk == "HIGH"
    assert result.recommended_reorder_quantity == 5


def test_medium_inventory_risk():
    result = calculate_inventory_risk(
        product_id="P001",
        current_inventory=27,
        predicted_demand=25,
    )

    assert result.inventory_risk == "MEDIUM"
    assert result.recommended_reorder_quantity == 0


def test_low_inventory_risk():
    result = calculate_inventory_risk(
        product_id="P001",
        current_inventory=35,
        predicted_demand=25,
    )

    assert result.inventory_risk == "LOW"
    assert result.recommended_reorder_quantity == 0


def test_reorder_quantity_when_inventory_is_low():
    quantity = calculate_reorder_quantity(
        current_inventory=20,
        predicted_demand=25,
    )

    assert quantity == 5


def test_reorder_quantity_never_negative():
    quantity = calculate_reorder_quantity(
        current_inventory=30,
        predicted_demand=25,
    )

    assert quantity == 0


def test_recommendation_when_inventory_is_low():
    result = get_inventory_recommendation(
        current_inventory=20,
        predicted_demand=25,
    )

    assert result == "REORDER"


def test_recommendation_when_inventory_needs_monitoring():
    result = get_inventory_recommendation(
        current_inventory=27,
        predicted_demand=25,
    )

    assert result == "MONITOR"


def test_recommendation_when_inventory_is_sufficient():
    result = get_inventory_recommendation(
        current_inventory=35,
        predicted_demand=25,
    )

    assert result == "SUFFICIENT"
