from services.supplier_service import (
    calculate_supplier_risk,
    create_supplier,
)


def test_low_supplier_risk():
    assert calculate_supplier_risk(
        reliability_score=90,
        lead_time_days=5,
    ) == "LOW"


def test_medium_supplier_risk():
    assert calculate_supplier_risk(
        reliability_score=75,
        lead_time_days=5,
    ) == "MEDIUM"


def test_high_supplier_risk():
    assert calculate_supplier_risk(
        reliability_score=50,
        lead_time_days=20,
    ) == "HIGH"


def test_create_supplier():
    supplier = create_supplier(
        supplier_id="S001",
        name="Global Components",
        country="India",
        lead_time_days=5,
        reliability_score=90,
        contact_email="supplier@example.com",
    )

    assert supplier.supplier_id == "S001"
    assert supplier.name == "Global Components"
    assert supplier.country == "India"
    assert supplier.lead_time_days == 5
    assert supplier.reliability_score == 90
    assert supplier.risk_level == "LOW"
    assert supplier.contact_email == "supplier@example.com"