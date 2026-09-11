from models.inventory import InventoryStatus

def calculate_inventory_risk(
    product_id: str,
    current_inventory: int,
    predicted_demand: float,
    reorder_point: int | None = None,
):
    if current_inventory < predicted_demand:
        risk = "HIGH"
    elif current_inventory < predicted_demand * 1.2:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return InventoryStatus(
        product_id=product_id,
        current_inventory=current_inventory,
        predicted_demand=round(predicted_demand, 2),
        inventory_risk=risk,
        recommended_reorder_quantity=calculate_reorder_quantity(
            current_inventory=current_inventory,
            predicted_demand=predicted_demand,
            reorder_point=reorder_point,
        ),
    )


def calculate_reorder_quantity(
    current_inventory: int,
    predicted_demand: float,
    reorder_point: int | None = None,
):
    target_inventory = (
        reorder_point
        if reorder_point is not None
        else predicted_demand
    )

    reorder_quantity = max(
        0,
        round(target_inventory - current_inventory)
    )

    return reorder_quantity


def get_inventory_recommendation(
    current_inventory: int,
    predicted_demand: float,
    reorder_point: int | None = None,
) -> str:
    if reorder_point is not None:
        if current_inventory < reorder_point:
            return "REORDER"
        return "SUFFICIENT"

    if current_inventory < predicted_demand:
        return "REORDER"

    if current_inventory < predicted_demand * 1.2:
        return "MONITOR"

    return "SUFFICIENT"


if __name__ == "__main__":
    current_inventory = 20
    predicted_demand = 22.48

    risk = calculate_inventory_risk(
        product_id="P001",
        current_inventory=current_inventory,
        predicted_demand=predicted_demand,
    )

    reorder_quantity = calculate_reorder_quantity(
        current_inventory=current_inventory,
        predicted_demand=predicted_demand,
    )

    print("Inventory Risk Analysis")
    print("-----------------------")
    print(risk)

    print()
    print("Reorder Recommendation")
    print("----------------------")
    print(f"Recommended reorder quantity: {reorder_quantity}")
