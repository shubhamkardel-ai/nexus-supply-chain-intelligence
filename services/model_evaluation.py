from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    root_mean_squared_error,
)


def evaluate_model(y_true, predictions):
    """
    Evaluate forecast predictions using MAE, RMSE, and MAPE.
    """

    mae = mean_absolute_error(
        y_true,
        predictions,
    )

    rmse = root_mean_squared_error(
        y_true,
        predictions,
    )

    mape = mean_absolute_percentage_error(
        y_true,
        predictions,
    ) * 100

    return {
        "mae": mae,
        "rmse": rmse,
        "mape": mape,
    }