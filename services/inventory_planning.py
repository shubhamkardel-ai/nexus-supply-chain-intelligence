import math
from pathlib import Path

from services.data_loader import load_csv


def calculate_safety_stock(
    demand_std_dev: float,
    lead_time_days: int,
    service_level_z: float = 1.65,
) -> int:
    """
    Calculate safety stock based on demand variability and lead time.
    """

    return math.ceil(
        service_level_z
        * demand_std_dev
        * math.sqrt(lead_time_days)
    )

def calculate_reorder_point(
    average_daily_demand: float,
    lead_time_days: int,
    safety_stock: int,
) -> int:
    """
    Calculate the inventory level at which a replenishment order should be placed.
    """

    return math.ceil(
        average_daily_demand * lead_time_days
        + safety_stock
    )

def calculate_demand_std_dev(
    demand_values,
) -> float:
    """
    Calculate the standard deviation of historical demand.
    """

    return float(demand_values.std())

def calculate_product_demand_std_dev(
    file_path: Path,
    product_id: str,
) -> float:
    """
    Calculate historical demand standard deviation for a product.
    """

    dataframe = load_csv(file_path)

    product_data = dataframe[
        dataframe["product_id"] == product_id
    ]

    if product_data.empty:
        raise ValueError(f"Product not found: {product_id}")

    return float(product_data["units_sold"].std())

def calculate_inventory_plan(
    average_daily_demand: float,
    demand_std_dev: float,
    lead_time_days: int,
    service_level_z: float = 1.65,
) -> dict:
    """
    Calculate the key inventory-planning values for a product.
    """

    safety_stock = calculate_safety_stock(
        demand_std_dev=demand_std_dev,
        lead_time_days=lead_time_days,
        service_level_z=service_level_z,
    )

    reorder_point = calculate_reorder_point(
        average_daily_demand=average_daily_demand,
        lead_time_days=lead_time_days,
        safety_stock=safety_stock,
    )

    lead_time_demand = math.ceil(
        average_daily_demand * lead_time_days
    )

    return {
        "average_daily_demand": round(average_daily_demand, 2),
        "demand_std_dev": round(demand_std_dev, 2),
        "lead_time_days": lead_time_days,
        "service_level_z": service_level_z,
        "lead_time_demand": lead_time_demand,
        "safety_stock": safety_stock,
        "reorder_point": reorder_point,
    }