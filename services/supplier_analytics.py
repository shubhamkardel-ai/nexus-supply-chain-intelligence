
def generate_supplier_analytics(
    suppliers: list,
    required_quantity: int,
    supplier_rankings: list,
) -> dict:
    """
    Analyze supplier costs, performance, eligibility,
    and procurement recommendation trade-offs.
    """

    if required_quantity <= 0:
        raise ValueError("Required quantity must be greater than zero.")

    if not suppliers:
        raise ValueError("At least one supplier is required.")

    if not supplier_rankings:
        raise ValueError("At least one eligible supplier is required.")

    # Build a lookup of eligible suppliers.
    eligible_ids = {
        ranking["supplier_id"]
        for ranking in supplier_rankings
    }

    # Analyze eligibility for every supplier.
    eligibility_results = []

    for supplier in suppliers:
        reasons = []

        if supplier.unit_cost is None:
            reasons.append("Unit cost is missing")
        elif supplier.unit_cost <= 0:
            reasons.append("Unit cost must be greater than zero")

        if supplier.capacity is None:
            reasons.append("Supplier capacity is missing")
        elif supplier.capacity < required_quantity:
            reasons.append("Insufficient supplier capacity")

        if supplier.minimum_order_quantity is None:
            reasons.append("Minimum order quantity is missing")
        elif supplier.minimum_order_quantity > required_quantity:
            reasons.append("Order quantity is below supplier minimum")

        is_eligible = supplier.supplier_id in eligible_ids

        eligibility_results.append({
            "supplier_id": supplier.supplier_id,
            "supplier_name": supplier.name,
            "eligible": is_eligible,
            "reasons": reasons if reasons else (
                [] if is_eligible else ["Supplier was not included in rankings"]
            ),
        })

    eligible_suppliers = [
        supplier for supplier in suppliers
        if supplier.supplier_id in eligible_ids
    ]

    # Analyze procurement costs.
    supplier_costs = [
        {
            "supplier_id": ranking["supplier_id"],
            "supplier_name": ranking["supplier_name"],
            "total_cost": ranking["total_cost"],
        }
        for ranking in supplier_rankings
    ]

    lowest_cost = min(
        supplier_costs,
        key=lambda item: item["total_cost"],
    )

    highest_cost = max(
        supplier_costs,
        key=lambda item: item["total_cost"],
    )

    recommended = supplier_rankings[0]

    # Analyze supplier performance.
    fastest_supplier = min(
        supplier_rankings,
        key=lambda item: item["lead_time_days"],
    )

    most_reliable_supplier = max(
        supplier_rankings,
        key=lambda item: item["reliability_score"],
    )

    # Recommendation explanation.
    recommendation_reasons = [
        f"Ranked first with an optimization score of "
        f"{recommended['optimization_score']:.4f}.",
        f"Total procurement cost is {recommended['total_cost']:.2f}.",
        f"Delivery lead time is {recommended['lead_time_days']} days.",
        f"Reliability score is {recommended['reliability_score']}.",
    ]

    trade_offs = []

    if recommended["supplier_id"] != lowest_cost["supplier_id"]:
        trade_offs.append(
            f"The recommended supplier is not the cheapest. "
            f"The lowest-cost option is {lowest_cost['supplier_name']}."
        )

    if recommended["supplier_id"] != fastest_supplier["supplier_id"]:
        trade_offs.append(
            f"The recommended supplier is not the fastest. "
            f"{fastest_supplier['supplier_name']} has the shortest lead time."
        )

    if recommended["supplier_id"] != most_reliable_supplier["supplier_id"]:
        trade_offs.append(
            f"The recommended supplier is not the most reliable. "
            f"{most_reliable_supplier['supplier_name']} has the highest reliability."
        )

    if not trade_offs:
        trade_offs.append(
            "The recommended supplier also leads in cost, delivery speed, "
            "and reliability among eligible suppliers."
        )

    return {
        "required_quantity": required_quantity,

        "cost_analysis": {
            "supplier_costs": supplier_costs,
            "lowest_cost_supplier": lowest_cost,
            "highest_cost_supplier": highest_cost,
            "cost_difference": round(
                highest_cost["total_cost"] - lowest_cost["total_cost"], 2
            ),
        },

        "performance_analysis": {
            "fastest_supplier": {
                "supplier_id": fastest_supplier["supplier_id"],
                "supplier_name": fastest_supplier["supplier_name"],
                "lead_time_days": fastest_supplier["lead_time_days"],
            },
            "most_reliable_supplier": {
                "supplier_id": most_reliable_supplier["supplier_id"],
                "supplier_name": most_reliable_supplier["supplier_name"],
                "reliability_score": most_reliable_supplier["reliability_score"],
            },
        },

        "eligibility_analysis": {
            "eligible_count": len(eligible_suppliers),
            "excluded_count": len(suppliers) - len(eligible_suppliers),
            "supplier_details": eligibility_results,
        },

        "recommendation_explanation": {
            "recommended_supplier": recommended["supplier_name"],
            "summary": (
                f"{recommended['supplier_name']} is the recommended supplier "
                f"based on the combined cost, delivery, and reliability ranking."
            ),
            "reasons": recommendation_reasons,
            "trade_offs": trade_offs,
        },
    }
