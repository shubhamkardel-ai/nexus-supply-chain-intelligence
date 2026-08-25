from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
)


def evaluate_model(y_true, predictions):
    """
    Evaluate forecast predictions using MAE and RMSE.
    """

    mae = mean_absolute_error(
        y_true,
        predictions,
    )

    rmse = root_mean_squared_error(
        y_true,
        predictions,
    )

    return {
        "mae": mae,
        "rmse": rmse,
    }