from dataclasses import dataclass


@dataclass
class Inventory:
    product_id: str
    product_name: str
    current_stock: int
    reorder_point: int
    safety_stock: int
    average_daily_demand: float
    supplier_id: str

    @property
    def stock_status(self) -> str:
        if self.current_stock <= self.reorder_point:
            return "CRITICAL"

        if self.current_stock <= self.reorder_point + self.safety_stock:
            return "LOW"

        return "HEALTHY"