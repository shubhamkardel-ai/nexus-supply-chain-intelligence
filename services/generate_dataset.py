from pathlib import Path

import numpy as np
import pandas as pd


def generate_sales_data(
    products: int = 20,
    days: int = 365,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate realistic synthetic daily sales data.
    """

    rng = np.random.default_rng(seed)

    dates = pd.date_range(
        start="2025-01-01",
        periods=days,
        freq="D",
    )

    records = []

    for product_number in range(1, products + 1):
        product_id = f"P{product_number:03d}"

        base_demand = rng.integers(20, 100)
        price = rng.choice([100, 150, 200, 250, 300, 400, 500])

        for current_date in dates:
            day_of_week = current_date.dayofweek

            weekend_factor = 1.15 if day_of_week >= 5 else 1.0

            seasonal_factor = (
                1
                + 0.15
                * np.sin(
                    2 * np.pi * current_date.dayofyear / 365
                )
            )

            noise = rng.normal(1.0, 0.10)

            units_sold = max(
                1,
                int(
                    base_demand
                    * weekend_factor
                    * seasonal_factor
                    * noise
                ),
            )

            customer_count = max(
                1,
                int(units_sold * rng.uniform(0.75, 0.95)),
            )

            revenue = units_sold * price

            records.append(
                {
                    "product_id": product_id,
                    "sale_date": current_date.strftime("%Y-%m-%d"),
                    "units_sold": units_sold,
                    "revenue": float(revenue),
                    "customer_count": customer_count,
                }
            )

    return pd.DataFrame(records)


if __name__ == "__main__":
    output_path = Path("data/sales.csv")

    dataframe = generate_sales_data()

    dataframe.to_csv(output_path, index=False)

    print("Dataset generated successfully!")
    print(f"Rows: {len(dataframe)}")
    print(f"Products: {dataframe['product_id'].nunique()}")
    print(
        f"Date range: "
        f"{dataframe['sale_date'].min()} → "
        f"{dataframe['sale_date'].max()}"
    )