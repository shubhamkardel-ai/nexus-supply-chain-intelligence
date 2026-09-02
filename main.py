from services.forecast_model import prepare_data, train_model
from pathlib import Path


def main():
    print("=" * 50)
    print("NEXUS SUPPLY CHAIN INTELLIGENCE")
    print("=" * 50)

    file_path = Path("data/sales.csv")

    X_train, X_test, y_train, y_test = prepare_data(file_path)

    model, preprocessor = train_model(
        X_train,
        y_train,
    )

    print()
    print("System Status")
    print("-" * 50)
    print("Forecasting Model : Ready")
    print("Inventory Service : Ready")
    print("API Service       : Ready")
    print("Model Type        : Random Forest")
    print(f"Training Samples  : {len(X_train)}")
    print(f"Testing Samples   : {len(X_test)}")
    print(f"Trees             : {len(model.estimators_)}")
    print()
    print("NEXUS system initialized successfully.")


if __name__ == "__main__":
    main()