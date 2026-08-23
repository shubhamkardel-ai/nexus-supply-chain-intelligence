from pathlib import Path

from services.forecast_model import (
    prepare_data,
    train_model,
)


def test_prepare_data():
    file_path = Path("data/sales.csv")

    X_train, X_test, y_train, y_test = prepare_data(file_path)

    assert len(X_train) > 0
    assert len(X_test) > 0
    assert len(y_train) == len(X_train)
    assert len(y_test) == len(X_test)


def test_train_model():
    file_path = Path("data/sales.csv")

    X_train, X_test, y_train, y_test = prepare_data(file_path)

    model, preprocessor = train_model(
        X_train,
        y_train,
    )

    assert model is not None
    assert preprocessor is not None
    assert len(model.estimators_) == 200