from pathlib import Path

from services.forecast_model import (
    prepare_data,
    train_model,
    predict_with_range,
)


def test_end_to_end_forecast_workflow():
    file_path = Path("data/sales.csv")

    # Prepare forecasting data
    X_train, X_test, y_train, y_test = prepare_data(file_path)

    assert len(X_train) > 0
    assert len(X_test) > 0
    assert len(y_train) == len(X_train)
    assert len(y_test) == len(X_test)

    # Train forecasting model
    model, preprocessor = train_model(
        X_train,
        y_train,
    )

    assert model is not None
    assert preprocessor is not None

    # Encode test data
    X_test_encoded = preprocessor.transform(X_test)

    # Generate prediction range
    prediction, lower_bound, upper_bound = predict_with_range(
        model,
        X_test_encoded,
    )

    # Validate forecast output
    assert prediction >= 0
    assert lower_bound >= 0
    assert upper_bound >= 0

    assert lower_bound <= prediction
    assert prediction <= upper_bound