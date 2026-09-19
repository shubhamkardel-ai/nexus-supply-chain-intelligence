from dataclasses import dataclass


@dataclass
class PurchaseOrderPlan:
    product_id: str
    supplier_id: str
    current_inventory: int
    predicted_demand: float
    reorder_point: int
    recommended_quantity: int
    order_required: bool