def analyze_disruption_impact(simulation_result: dict) -> dict:
    """
    Converts a disruption simulation result into a business impact assessment.
    """

    shortage = simulation_result.get("expected_shortage", 0)
    projected_inventory = simulation_result.get("projected_inventory", 0)
    risk_level = simulation_result.get("risk_level", "LOW")

    if shortage > 0:
        impact_level = "HIGH"
        recommendation = (
            "Urgent replenishment is recommended. "
            "Consider an alternative supplier or emergency sourcing."
        )

    elif risk_level == "MEDIUM":
        impact_level = "MEDIUM"
        recommendation = (
            "Monitor inventory closely and consider increasing safety stock."
        )

    elif projected_inventory <= 0:
        impact_level = "HIGH"
        recommendation = (
            "Inventory depletion is likely. Plan replenishment immediately."
        )

    else:
        impact_level = "LOW"
        recommendation = (
            "Current supply chain position is stable. Continue monitoring."
        )

    return {
        "product_id": simulation_result.get("product_id"),
        "disruption_type": simulation_result.get("disruption_type"),
        "impact_level": impact_level,
        "expected_shortage": shortage,
        "projected_inventory": projected_inventory,
        "recommendation": recommendation,
    }