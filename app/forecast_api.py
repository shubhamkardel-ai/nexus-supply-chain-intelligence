from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

from services.inventory_service import calculate_inventory_risk

from services.forecast_model import (
    prepare_data,
    train_model,
    predict_with_range,
)

app = FastAPI(
    title="NEXUS Supply Chain Intelligence",
    description="AI-powered demand forecasting API",
    version="1.0.0",
)


class ForecastRequest(BaseModel):
    product_id: str = Field(..., min_length=1)
    day_of_week: int = Field(..., ge=0, le=6)
    day_of_month: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    revenue_per_unit: float = Field(..., ge=0)
    units_per_customer: float = Field(..., ge=0)
    lag_1: float = Field(..., ge=0)
    lag_7: float = Field(..., ge=0)
    rolling_mean_7: float = Field(..., ge=0)
    rolling_mean_30: float = Field(..., ge=0)
    current_inventory: int = Field(..., ge=0)

class ForecastResponse(BaseModel):
    product_id: str
    predicted_units_sold: float
    forecast_lower: float
    forecast_upper: float
    forecast_type: str
    model: str
    inventory_risk: str
    current_inventory: int
    recommended_reorder_quantity: int


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

@app.get("/inventory/status")
def inventory_status():
    return {
        "service": "inventory_management",
        "status": "active",
    }

@app.post("/forecast", response_model=ForecastResponse)
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

    prediction, lower_bound, upper_bound = predict_with_range(
        model,
        encoded_data,
    )

    inventory_analysis = calculate_inventory_risk(
        product_id=request.product_id,
        current_inventory=request.current_inventory,
        predicted_demand=prediction,
    )

    return {
        "product_id": request.product_id,
        "predicted_units_sold": round(float(prediction), 2),
        "forecast_lower": round(float(lower_bound), 2),
        "forecast_upper": round(float(upper_bound), 2),
        "forecast_type": "demand_forecast",
        "model": "Random Forest",
        "inventory_risk": inventory_analysis.inventory_risk,
        "current_inventory": inventory_analysis.current_inventory,
        "recommended_reorder_quantity": inventory_analysis.recommended_reorder_quantity,
    }