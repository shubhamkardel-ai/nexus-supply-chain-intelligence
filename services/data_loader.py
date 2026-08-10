from pathlib import Path

import pandas as pd


def load_csv(file_path: Path) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    return pd.read_csv(file_path)


def save_csv(dataframe: pd.DataFrame, file_path: Path) -> None:
    """
    Save a DataFrame as a CSV file.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(file_path, index=False)


if __name__ == "__main__":
    file_path = Path("data/sales.csv")

    df = load_csv(file_path)

    print(df)
    print("\nColumns:")
    print(df.columns.tolist())