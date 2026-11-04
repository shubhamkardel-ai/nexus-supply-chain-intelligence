from models.disruption import DisruptionScenario
from services.disruption_service import simulate_disruption


def test_demand_spike():
    scenario = DisruptionScenario(
        product_id="P001",
        disruption_type="demand_spike",
        severity_percent=30,
        duration_days=7,
    )

    result = simulate_disruption(
        scenario,
        base_demand=20,
        base_lead_time=5,
        current_inventory=200,
    )

    assert result["simulated_demand"] == 26
    assert result["risk_level"] in ["LOW", "MEDIUM", "HIGH"]


def test_supplier_delay():
    scenario = DisruptionScenario(
        product_id="P001",
        disruption_type="supplier_delay",
        severity_percent=50,
        duration_days=7,
    )

    result = simulate_disruption(
        scenario,
        base_demand=20,
        base_lead_time=4,
        current_inventory=200,
    )

    assert result["simulated_lead_time"] == 6


def test_inventory_shortage():
    scenario = DisruptionScenario(
        product_id="P001",
        disruption_type="inventory_shortage",
        severity_percent=50,
        duration_days=5,
    )

    result = simulate_disruption(
        scenario,
        base_demand=20,
        base_lead_time=5,
        current_inventory=200,
    )

    assert result["projected_inventory"] == 0
    assert result["expected_shortage"] == 0


def test_supplier_unavailable():
    scenario = DisruptionScenario(
        product_id="P001",
        disruption_type="supplier_unavailable",
        severity_percent=0,
        duration_days=10,
    )

    result = simulate_disruption(
        scenario,
        base_demand=20,
        base_lead_time=5,
        current_inventory=100,
    )

    assert result["simulated_lead_time"] == 15
    assert result["expected_shortage"] == 100