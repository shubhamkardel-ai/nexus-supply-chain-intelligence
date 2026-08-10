from dataclasses import dataclass
from typing import Optional


@dataclass
class Supplier:
    supplier_id: str
    name: str
    country: str
    lead_time_days: int
    reliability_score: float
    risk_level: str
    contact_email: Optional[str] = None