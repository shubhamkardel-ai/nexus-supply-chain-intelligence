from models.disruption import DisruptionScenario


def simulate_disruption(
    scenario: DisruptionScenario,
    base_demand: float,
    base_lead_time: int,
    current_inventory: int,
) -> dict:
    """
    Simulates the impact of a supply chain disruption.
    """

    severity = scenario.severity_percent / 100

    simulated_demand = base_demand
    simulated_lead_time = base_lead_time
    inventory_impact = current_inventory

    if scenario.disruption_type == "demand_spike":
        simulated_demand = base_demand * (1 + severity)

    elif scenario.disruption_type == "supplier_delay":
        simulated_lead_time = round(
            base_lead_time * (1 + severity)
        )

    elif scenario.disruption_type == "inventory_shortage":
        inventory_impact = max(
            0,
            round(current_inventory * (1 - severity))
        )

    elif scenario.disruption_type == "supplier_unavailable":
        simulated_lead_time = (
            base_lead_time + scenario.duration_days
        )

    expected_demand = simulated_demand * scenario.duration_days

    projected_inventory = max(
        0,
        inventory_impact - round(expected_demand),
    )

    shortage = max(
        0,
        round(expected_demand - inventory_impact),
    )

    if shortage > 0:
        risk_level = "HIGH"
    elif projected_inventory < simulated_demand:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "product_id": scenario.product_id,
        "disruption_type": scenario.disruption_type,
        "duration_days": scenario.duration_days,
        "simulated_demand": round(simulated_demand, 2),
        "simulated_lead_time": simulated_lead_time,
        "projected_inventory": projected_inventory,
        "expected_demand": round(expected_demand, 2),
        "expected_shortage": shortage,
        "risk_level": risk_level,
    }