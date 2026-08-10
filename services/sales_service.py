from datetime import datetime
from pathlib import Path

from models.sales import SalesRecord
from services.data_loader import load_csv


def load_sales_records(file_path: Path) -> list[SalesRecord]:
    """
    Load sales data from CSV and convert each row into a SalesRecord.
    """
    dataframe = load_csv(file_path)

    records = []

    for _, row in dataframe.iterrows():
        record = SalesRecord(
            product_id=row["product_id"],
            sale_date=datetime.strptime(
                row["sale_date"], "%Y-%m-%d"
            ).date(),
            units_sold=int(row["units_sold"]),
            revenue=float(row["revenue"]),
            customer_count=int(row["customer_count"]),
        )

        records.append(record)

    return records


if __name__ == "__main__":
    file_path = Path("data/sales.csv")

    records = load_sales_records(file_path)

    for record in records:
        print(record)