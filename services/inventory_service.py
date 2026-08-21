def calculate_inventory_risk(
    current_inventory: int,
    predicted_demand: float,
):
    if current_inventory < predicted_demand:
        risk = "HIGH"
    elif current_inventory < predicted_demand * 1.2:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "current_inventory": current_inventory,
        "predicted_demand": round(predicted_demand, 2),
        "inventory_risk": risk,
    }


def calculate_reorder_quantity(
    current_inventory: int,
    predicted_demand: float,
):
    reorder_quantity = max(
        0,
        round(predicted_demand - current_inventory)
    )

    return reorder_quantity


if __name__ == "__main__":
    current_inventory = 20
    predicted_demand = 22.48

    risk = calculate_inventory_risk(
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