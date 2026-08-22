from dataclasses import dataclass


@dataclass
class InventoryStatus:
    product_id: str
    current_inventory: int
    predicted_demand: float
    inventory_risk: str
    recommended_reorder_quantity: int