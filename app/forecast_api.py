from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from services.forecast_model import prepare_data, train_model


app = FastAPI(
    title="NEXUS Supply Chain Intelligence",
    description="AI-powered demand forecasting API",
    version="1.0.0",
)


class ForecastRequest(BaseModel):
    product_id: str
    day_of_week: int
    day_of_month: int
    month: int
    revenue_per_unit: float
    units_per_customer: float
    lag_1: float
    lag_7: float
    rolling_mean_7: float
    rolling_mean_30: float


# Train the model when the API starts
file_path = Path("data/sales.csv")

X_train, X_test, y_train, y_test = prepare_data(file_path)
model, preprocessor = train_model(X_train, y_train)


@app.get("/")
def root():
    return {
        "project": "NEXUS Supply Chain Intelligence",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.post("/forecast")
def forecast(request: ForecastRequest):
    input_data = pd.DataFrame(
        [
            {
                "product_id": request.product_id,
                "day_of_week": request.day_of_week,
                "day_of_month": request.day_of_month,
                "month": request.month,
                "revenue_per_unit": request.revenue_per_unit,
                "units_per_customer": request.units_per_customer,
                "lag_1": request.lag_1,
                "lag_7": request.lag_7,
                "rolling_mean_7": request.rolling_mean_7,
                "rolling_mean_30": request.rolling_mean_30,
            }
        ]
    )

    encoded_data = preprocessor.transform(input_data)

    prediction = model.predict(encoded_data)[0]

    return {
        "product_id": request.product_id,
        "predicted_units_sold": round(float(prediction), 2),
    }