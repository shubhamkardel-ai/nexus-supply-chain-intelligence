from dataclasses import dataclass


@dataclass
class DisruptionScenario:
    product_id: str
    disruption_type: str
    severity_percent: float
    duration_days: int