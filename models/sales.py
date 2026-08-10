from dataclasses import dataclass
from datetime import date


@dataclass
class SalesRecord:
    product_id: str
    sale_date: date
    units_sold: int
    revenue: float
    customer_count: int


if __name__ == "__main__":
    record = SalesRecord(
        product_id="P001",
        sale_date=date(2026, 1, 1),
        units_sold=10,
        revenue=2500.0,
        customer_count=8,
    )

    print(record)