from models.supplier import Supplier


def calculate_supplier_risk(
    reliability_score: float,
    lead_time_days: int,
) -> str:
    if reliability_score < 60 or lead_time_days > 14:
        return "HIGH"

    if reliability_score < 80 or lead_time_days > 7:
        return "MEDIUM"

    return "LOW"


def create_supplier(
    supplier_id: str,
    name: str,
    country: str,
    lead_time_days: int,
    reliability_score: float,
    contact_email: str | None = None,
) -> Supplier:
    risk_level = calculate_supplier_risk(
        reliability_score=reliability_score,
        lead_time_days=lead_time_days,
    )

    return Supplier(
        supplier_id=supplier_id,
        name=name,
        country=country,
        lead_time_days=lead_time_days,
        reliability_score=reliability_score,
        risk_level=risk_level,
        contact_email=contact_email,
    )