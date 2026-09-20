from services.scenario_service import calculate_scenario


def test_demand_increase_scenario():
    result = calculate_scenario(
        product_id="P001",
        base_demand=30,
        base_lead_time=7,
        base_reorder_point=220,
        demand_change_percent=20,
    )

    assert result.adjusted_demand == 36
    assert result.adjusted_lead_time == 7
    assert result.demand_change_percent == 20
    assert result.lead_time_change_percent == 0


def test_lead_time_increase_scenario():
    result = calculate_scenario(
        product_id="P001",
        base_demand=30,
        base_lead_time=7,
        base_reorder_point=220,
        lead_time_change_percent=100,
    )

    assert result.adjusted_lead_time == 14
    assert result.adjusted_demand == 30
    assert result.lead_time_change_percent == 100


def test_combined_scenario():
    result = calculate_scenario(
        product_id="P002",
        base_demand=25,
        base_lead_time=4,
        base_reorder_point=120,
        demand_change_percent=20,
        lead_time_change_percent=50,
    )

    assert result.adjusted_demand == 30
    assert result.adjusted_lead_time == 6
    assert result.base_reorder_point == 120


def test_no_change_scenario():
    result = calculate_scenario(
        product_id="P003",
        base_demand=40,
        base_lead_time=5,
        base_reorder_point=220,
    )

    assert result.adjusted_demand == 40
    assert result.adjusted_lead_time == 5
    assert result.adjusted_reorder_point == 220