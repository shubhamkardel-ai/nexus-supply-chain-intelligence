from services.model_evaluation import evaluate_model


def test_evaluate_model_returns_metrics():
    y_true = [10, 20, 30]
    predictions = [12, 18, 29]

    metrics = evaluate_model(
        y_true,
        predictions,
    )

    assert "mae" in metrics
    assert "rmse" in metrics


def test_evaluate_model_metrics_are_non_negative():
    y_true = [10, 20, 30]
    predictions = [12, 18, 29]

    metrics = evaluate_model(
        y_true,
        predictions,
    )

    assert metrics["mae"] >= 0
    assert metrics["rmse"] >= 0