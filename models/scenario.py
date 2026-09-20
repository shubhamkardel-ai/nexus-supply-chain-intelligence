from dataclasses import dataclass


@dataclass
class ScenarioResult:
    product_id: str
    base_demand: float
    adjusted_demand: float
    base_lead_time: int
    adjusted_lead_time: int
    base_reorder_point: int
    adjusted_reorder_point: int
    demand_change_percent: float
    lead_time_change_percent: float