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