
def optimize_supplier_selection(
    suppliers: list,
    required_quantity: int,
) -> dict:
    """
    Select the best feasible supplier using cost,
    reliability, and delivery lead time.

    Lower optimization scores are better.
    """

    if required_quantity <= 0:
        raise ValueError("Required quantity must be greater than zero.")

    # Find suppliers that can fulfill the order
    eligible_suppliers = []

    for supplier in suppliers:

        if (
            supplier.unit_cost is None
            or supplier.capacity is None
            or supplier.minimum_order_quantity is None
        ):
            continue

        if supplier.unit_cost <= 0:
            continue

        if supplier.capacity < required_quantity:
            continue

        if supplier.minimum_order_quantity > required_quantity:
            continue

        eligible_suppliers.append(supplier)

    if not eligible_suppliers:
        raise ValueError("No supplier can fulfill the required quantity.")

    # Calculate total procurement cost
    total_costs = [
        supplier.unit_cost * required_quantity
        for supplier in eligible_suppliers
    ]

    lead_times = [
        supplier.lead_time_days
        for supplier in eligible_suppliers
    ]

    reliability_scores = [
        supplier.reliability_score
        for supplier in eligible_suppliers
    ]

    # Normalize values so different units can be compared
    def normalize(value, minimum, maximum):
        if maximum == minimum:
            return 0.0

        return (value - minimum) / (maximum - minimum)

    evaluated_suppliers = []

    for supplier in eligible_suppliers:

        total_cost = supplier.unit_cost * required_quantity

        cost_score = normalize(
            total_cost,
            min(total_costs),
            max(total_costs),
        )

        lead_time_score = normalize(
            supplier.lead_time_days,
            min(lead_times),
            max(lead_times),
        )

        reliability_score = 1 - normalize(
            supplier.reliability_score,
            min(reliability_scores),
            max(reliability_scores),
        )

        # Equal importance: cost, lead time, reliability
        final_score = (
            cost_score * 0.40
            + lead_time_score * 0.30
            + reliability_score * 0.30
        )

        evaluated_suppliers.append({
            "supplier": supplier,
            "total_cost": round(total_cost, 2),
            "optimization_score": round(final_score, 4),
        })

    # Lowest score represents the best overall option
    evaluated_suppliers.sort(
        key=lambda item: (
            item["optimization_score"],
            item["total_cost"],
        )
    )

    best = evaluated_suppliers[0]
    supplier = best["supplier"]

    return {
        "supplier_id": supplier.supplier_id,
        "supplier_name": supplier.name,
        "required_quantity": required_quantity,
        "unit_cost": supplier.unit_cost,
        "total_cost": best["total_cost"],
        "lead_time_days": supplier.lead_time_days,
        "reliability_score": supplier.reliability_score,
        "optimization_score": best["optimization_score"],
    }
