from services.purchase_planning import calculate_purchase_plan


def test_purchase_required():
    result = calculate_purchase_plan(
        product_id="P001",
        supplier_id="S001",
        current_inventory=50,
        predicted_demand=30,
        reorder_point=100,
    )

    assert result.order_required is True
    assert result.recommended_quantity == 80


def test_purchase_not_required():
    result = calculate_purchase_plan(
        product_id="P001",
        supplier_id="S001",
        current_inventory=150,
        predicted_demand=30,
        reorder_point=100,
    )

    assert result.order_required is False
    assert result.recommended_quantity == 0


def test_purchase_plan_fields():
    result = calculate_purchase_plan(
        product_id="P002",
        supplier_id="S002",
        current_inventory=40,
        predicted_demand=25.5,
        reorder_point=80,
    )

    assert result.product_id == "P002"
    assert result.supplier_id == "S002"
    assert result.current_inventory == 40
    assert result.predicted_demand == 25.5
    assert result.reorder_point == 80