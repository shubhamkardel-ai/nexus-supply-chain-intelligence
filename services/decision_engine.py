def generate_decision(impact_result: dict) -> dict:
    """
    Selects the best supply chain response based on disruption impact.
    """

    impact_level = impact_result.get("impact_level", "LOW")
    expected_shortage = impact_result.get("expected_shortage", 0)
    projected_inventory = impact_result.get("projected_inventory", 0)

    if impact_level == "HIGH" and expected_shortage >= 100:
        action = "EMERGENCY_SOURCING"
        priority = "CRITICAL"
        rationale = (
            "A significant inventory shortage is expected. "
            "Emergency sourcing is recommended to reduce supply disruption."
        )

    elif impact_level == "HIGH":
        action = "ALTERNATIVE_SUPPLIER"
        priority = "HIGH"
        rationale = (
            "The disruption creates a significant supply risk. "
            "Consider shifting orders to an alternative supplier."
        )

    elif impact_level == "MEDIUM":
        action = "REORDER"
        priority = "MEDIUM"
        rationale = (
            "Supply conditions require replenishment. "
            "Place an order and monitor inventory closely."
        )

    else:
        action = "MONITOR"
        priority = "LOW"
        rationale = (
            "The current disruption has limited business impact. "
            "Continue monitoring supply chain conditions."
        )

    return {
        "product_id": impact_result.get("product_id"),
        "disruption_type": impact_result.get("disruption_type"),
        "impact_level": impact_level,
        "expected_shortage": expected_shortage,
        "projected_inventory": projected_inventory,
        "recommended_action": action,
        "priority": priority,
        "rationale": rationale,
    }