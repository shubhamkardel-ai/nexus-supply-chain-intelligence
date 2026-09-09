import pandas as pd
from pathlib import Path
from services.inventory_planning import (
    calculate_demand_std_dev,
    calculate_safety_stock,
    calculate_reorder_point,
    calculate_product_demand_std_dev,
)



def test_calculate_safety_stock():
    result = calculate_safety_stock(
        demand_std_dev=5,
        lead_time_days=7,
    )

    assert result == 22


def test_calculate_reorder_point():
    result = calculate_reorder_point(
        average_daily_demand=25,
        lead_time_days=7,
        safety_stock=22,
    )

    assert result == 197

def test_calculate_demand_std_dev():
    demand_values = pd.Series([20, 25, 30, 25, 20])

    result = calculate_demand_std_dev(demand_values)

    assert round(result, 2) == 4.18

def test_calculate_product_demand_std_dev():
    result = calculate_product_demand_std_dev(
        Path("data/sales.csv"),
        "P001",
    )

    assert round(result, 2) == 4.49