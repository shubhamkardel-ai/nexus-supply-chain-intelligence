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


if __name__ == "__main__":
    result = calculate_inventory_risk(
        current_inventory=20,
        predicted_demand=22.48,
    )

    print("Inventory Risk Analysis")
    print("-----------------------")
    print(result)