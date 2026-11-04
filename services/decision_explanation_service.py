
def explain_decision(impact_result: dict, decision_result: dict) -> dict:
    """
    Explain a supply chain decision using actual impact and decision results.
    """

    required_impact_fields = [
        "impact_level",
        "expected_shortage",
        "projected_inventory",
    ]

    required_decision_fields = [
        "product_id",
        "recommended_action",
        "priority",
    ]

    for field in required_impact_fields:
        if field not in impact_result:
            raise ValueError(f"Missing impact field: {field}")

    for field in required_decision_fields:
        if field not in decision_result:
            raise ValueError(f"Missing decision field: {field}")

    impact_level = impact_result["impact_level"]
    shortage = impact_result["expected_shortage"]
    inventory = impact_result["projected_inventory"]

    action = decision_result["recommended_action"]
    priority = decision_result["priority"]

    # Explain the selected action.
    explanations = {
        "EMERGENCY_SOURCING": (
            "Emergency sourcing was selected because the impact is HIGH "
            "and the expected shortage is at least 100 units."
        ),
        "ALTERNATIVE_SUPPLIER": (
            "An alternative supplier was selected because the impact is HIGH, "
            "but the shortage does not meet the emergency sourcing threshold."
        ),
        "REORDER": (
            "Reordering was selected because the supply chain impact is MEDIUM."
        ),
        "MONITOR": (
            "Monitoring was selected because the current impact is LOW."
        ),
    }

    if action not in explanations:
        raise ValueError(f"Unsupported recommended action: {action}")

    # Identify the evidence behind the decision.
    key_factors = [
        {
            "factor": "Impact Level",
            "value": impact_level,
            "effect": f"The disruption has a {impact_level} impact."
        },
        {
            "factor": "Expected Shortage",
            "value": shortage,
            "effect": (
                "A shortage is expected."
                if shortage > 0
                else "No shortage is currently expected."
            )
        },
        {
            "factor": "Projected Inventory",
            "value": inventory,
            "effect": (
                "Projected inventory is negative."
                if inventory < 0
                else "Projected inventory is non-negative."
            )
        },
    ]

    # Explain why other actions were not selected.
    alternatives = []

    if action != "EMERGENCY_SOURCING":
        alternatives.append({
            "action": "EMERGENCY_SOURCING",
            "reason": (
                "Not selected because the decision conditions for emergency "
                "sourcing were not met."
            )
        })

    if action != "ALTERNATIVE_SUPPLIER":
        alternatives.append({
            "action": "ALTERNATIVE_SUPPLIER",
            "reason": (
                "Not selected because the current decision rules did not "
                "prioritize alternative sourcing."
            )
        })

    if action != "REORDER":
        alternatives.append({
            "action": "REORDER",
            "reason": (
                "Not selected because the impact level did not trigger "
                "the reorder rule."
            )
        })

    if action != "MONITOR":
        alternatives.append({
            "action": "MONITOR",
            "reason": "Not selected because a higher-priority response was required."
        })

    return {
        "product_id": decision_result["product_id"],
        "recommended_action": action,
        "priority": priority,
        "decision_summary": explanations[action],
        "key_factors": key_factors,
        "alternatives_considered": alternatives,
        "supporting_evidence": {
            "impact_level": impact_level,
            "expected_shortage": shortage,
            "projected_inventory": inventory,
        },
    }
