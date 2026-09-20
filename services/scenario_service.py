from models.scenario import ScenarioResult


def calculate_scenario(
    product_id: str,
    base_demand: float,
    base_lead_time: int,
    base_reorder_point: int,
    demand_change_percent: float = 0,
    lead_time_change_percent: float = 0,
) -> ScenarioResult:
    adjusted_demand = base_demand * (
        1 + demand_change_percent / 100
    )

    adjusted_lead_time = max(
        1,
        round(
            base_lead_time
            * (1 + lead_time_change_percent / 100)
        ),
    )

    demand_difference = adjusted_demand - base_demand
    lead_time_difference = (
        adjusted_lead_time - base_lead_time
    )

    adjusted_reorder_point = max(
        0,
        round(
            base_reorder_point
            + demand_difference * adjusted_lead_time
            + base_demand * lead_time_difference
        ),
    )

    return ScenarioResult(
        product_id=product_id,
        base_demand=round(base_demand, 2),
        adjusted_demand=round(adjusted_demand, 2),
        base_lead_time=base_lead_time,
        adjusted_lead_time=adjusted_lead_time,
        base_reorder_point=base_reorder_point,
        adjusted_reorder_point=adjusted_reorder_point,
        demand_change_percent=demand_change_percent,
        lead_time_change_percent=lead_time_change_percent,
    )