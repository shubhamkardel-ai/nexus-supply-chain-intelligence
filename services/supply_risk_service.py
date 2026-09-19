from models.supply_risk import SupplyRisk


def calculate_demand_risk(
    current_inventory: int,
    predicted_demand: float,
) -> str:
    if current_inventory < predicted_demand:
        return "HIGH"

    if current_inventory < predicted_demand * 1.2:
        return "MEDIUM"

    return "LOW"


def calculate_supply_risk(
    product_id: str,
    supplier_id: str,
    current_inventory: int,
    predicted_demand: float,
    supplier_risk: str,
) -> SupplyRisk:
    demand_risk = calculate_demand_risk(
        current_inventory=current_inventory,
        predicted_demand=predicted_demand,
    )

    risk_weights = {
        "LOW": 20,
        "MEDIUM": 50,
        "HIGH": 80,
    }

    demand_score = risk_weights[demand_risk]
    supplier_score = risk_weights[supplier_risk]

    risk_score = round(
        demand_score * 0.6 + supplier_score * 0.4,
        2,
    )

    if risk_score >= 70:
        overall_risk = "HIGH"
    elif risk_score >= 40:
        overall_risk = "MEDIUM"
    else:
        overall_risk = "LOW"

    return SupplyRisk(
        product_id=product_id,
        supplier_id=supplier_id,
        demand_risk=demand_risk,
        supplier_risk=supplier_risk,
        overall_risk=overall_risk,
        risk_score=risk_score,
    )