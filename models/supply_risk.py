from dataclasses import dataclass


@dataclass
class SupplyRisk:
    product_id: str
    supplier_id: str
    demand_risk: str
    supplier_risk: str
    overall_risk: str
    risk_score: float