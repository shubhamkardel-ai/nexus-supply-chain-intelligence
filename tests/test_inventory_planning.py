import pandas as pd
from pathlib import Path
from services.inventory_planning import (
    calculate_demand_std_dev,
    calculate_inventory_plan,
    calculate_product_demand_std_dev,
    calculate_reorder_point,
    calculate_safety_stock,
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

def test_calculate_inventory_plan():
    result = calculate_inventory_plan(
        average_daily_demand=25,
        demand_std_dev=4,
        lead_time_days=4,
        service_level_z=1.65,
    )

    assert result["average_daily_demand"] == 25
    assert result["demand_std_dev"] == 4
    assert result["lead_time_days"] == 4
    assert result["lead_time_demand"] == 100
    assert result["safety_stock"] == 14
    assert result["reorder_point"] == 114