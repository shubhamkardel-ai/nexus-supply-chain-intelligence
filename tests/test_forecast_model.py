from pathlib import Path

from services.forecast_model import (
    prepare_data,
    train_model,
    predict_with_range,
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


def test_predict_with_range():
    file_path = Path("data/sales.csv")

    X_train, X_test, y_train, y_test = prepare_data(file_path)

    model, preprocessor = train_model(
        X_train,
        y_train,
    )

    encoded_data = preprocessor.transform(
        X_test.iloc[[0]]
    )

    prediction, lower_bound, upper_bound = predict_with_range(
        model,
        encoded_data,
    )

    assert prediction >= 0
    assert lower_bound <= prediction
    assert upper_bound >= prediction


def test_model_predictions_are_valid():
    file_path = Path("data/sales.csv")

    X_train, X_test, y_train, y_test = prepare_data(file_path)

    model, preprocessor = train_model(
        X_train,
        y_train,
    )

    X_test_encoded = preprocessor.transform(X_test)

    predictions = model.predict(X_test_encoded)

    assert len(predictions) == len(y_test)
    assert all(prediction >= 0 for prediction in predictions)
    assert predictions.max() < 1000