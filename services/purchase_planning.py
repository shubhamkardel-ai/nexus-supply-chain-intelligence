from models.purchase_order import PurchaseOrderPlan


def calculate_purchase_plan(
    product_id: str,
    supplier_id: str,
    current_inventory: int,
    predicted_demand: float,
    reorder_point: int,
) -> PurchaseOrderPlan:
    order_required = current_inventory < reorder_point

    recommended_quantity = max(
        0,
        round(predicted_demand + reorder_point - current_inventory),
    )

    if not order_required:
        recommended_quantity = 0

    return PurchaseOrderPlan(
        product_id=product_id,
        supplier_id=supplier_id,
        current_inventory=current_inventory,
        predicted_demand=round(predicted_demand, 2),
        reorder_point=reorder_point,
        recommended_quantity=recommended_quantity,
        order_required=order_required,
    )